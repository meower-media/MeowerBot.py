import asyncio
import copy
import json
import logging
import secrets
import shlex
import traceback
from enum import StrEnum
from typing import Optional, Callable, Dict, List

import httpx

from ._cache import Cache
from .api import MeowerAPI
from .cl import Client
from .cog import Cog
from .command import AppCommand
from .context import Context, PartialChat, PartialUser, Post, User
from .data.generic import UUID
from types import CoroutineType

from .events import Events


class CallBackIds(StrEnum):
	"""Callbacks that the bot calls. You can find more documentation in :class:`MeowerBot.bot.Bot`"""
	error = "error"
	__raw__ = "__raw__"
	login = "login"
	disconnect = "disconnect"
	ulist = "ulist"
	message = "message"
	raw_message = "raw_message"
	direct = "direct"
	statuscode = "statuscode"

cbids = CallBackIds
callbacks = [i for i in CallBackIds] # type: ignore


class Bot(Client, Events):
	"""A class that holds all the networking for a Meower bot to function and run"""

	messages: List[Post] = []  #: :meta private: :meta hide-value:
	post_condition = asyncio.Condition() #: :meta private: :meta hide-value:
	user: PartialUser | User # Parcial user when bot is not logged in
	cache: Cache

	__bridges__ = [  #: :meta public: :meta hide-value:
		"Discord",
		"Revower",
		"revolt"
	]


	BOT_NO_PMSG_RESPONSE = [ #: :meta private: :meta hide-value:
		"I:500 | Bot",
		"I: 500 | Bot",
		"I: 100 | Bot",
		"I: 100 | Bot"
	]

	@property
	def latency(self) -> float:
		"""Gets the latency of the bot

		:return: Bot latency
		:rtype: int
		"""
		return self.ws.latency

	async def _t_ping(self):
		while True:
			try:
				await asyncio.sleep(5)

				await self.send_packet({"cmd": "ping", "val": ""})
			except Exception as e:
				await self._error(e)
				break

	def __init__(self, prefix=None):  # type: ignore

		super().__init__()
		self.api: MeowerAPI = None  # type: ignore
		self.callbacks: Dict[str, List[CoroutineType]] = {str(i): [] for i in callbacks}
		self.callbacks["__raw__"] = []
		self.userlist = []

		# to be used in start
		self.username: str  = None # type: ignore #: :meta hide-value:
		self.password: str  = None # type: ignore #: :meta hide-value:

		self.commands = {}
		self.prefix = prefix
		self.logger = logging.getLogger("MeowerBot")
		self.server: str  = None  # type: ignore
		self.cache = Cache()

		self.cogs: Dict[str, Cog] = {}
	# Interface

	def event(self, func: Callable):
		"""Creates a callback that takes over the original functionality of the bot.

		Valid callbacks are defined in :class:`CallBackIds`

		:param func: The callback function
		:type func: Callable
		:raises TypeError: The func provided does not have a valid callback name
		"""
		if func.__name__ not in callbacks:
			raise TypeError(f"{func.__name__} is not a valid callback")

		setattr(self, func.__name__, func)

	def listen(self, callback: Optional[str] = None):
		"""
		Does the same thing as :meth MeowerBot.bot.Bot.event:but does not replace the bot's original functionality

		Valid callbacks are defined in :class:`CallBackIds`
		:raises TypeError: The listener provided is not valid
		"""
		def inner(func):
			nonlocal callback
			callback = callback if callback is not None else func.__name__

			if callback not in callbacks:
				raise TypeError(f"{callback} is not a valid listener")

			self.callbacks[callback].append(func)

			return func
		return inner

	def update_commands(self):
		for cog in self.cogs.values():
			cog.update_commands()

			self.commands.update(cog.commands)
			for i in cog.callbacks.keys():
				self.callbacks[str(i)].append(cog.callbacks[str(i)])

	async def error(self, err: Exception):
		"""Handles errors for the bot.

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		self.logger.error(traceback.print_exception(err))

	async def message(self, message: Post):
		"""Method for overiding how the bot handles messages.

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		message = await self.handle_bridges(message)

		if not message.data.startswith(self.prefix):
			return

		message.data = message.data.removeprefix(self.prefix)

		await self.run_commands(message)

	async def _run_event(self, event: cbids, *args, **kwargs):
		events: List[Callable] = [getattr(self, str(event))]

		for i in self.callbacks[str(event)]:
			if type(i) is list:
				events.extend(i) # type: ignore
			elif callable(i):  # Check if the element is Callable
				events.append(i)

		err = await asyncio.gather(*[i(*args, **kwargs) for i in events if callable(i)], return_exceptions=True)
		for i in err:
			if i is not None:
				if isinstance(i, Exception) and event != cbids.error:
					await self._error(i)


	# websocket

	async def send_packet(self, message: dict):
		if message.get("listener") != "mb.py_login":
			self.logger.debug("Sending Packet:  " + json.dumps(message))
		else:
			message_sensitive = copy.deepcopy(message)
			message_sensitive["val"]["val"]["pswd"] = "<PASSWORD>"
			self.logger.debug("Sending Packet:  " + json.dumps(message_sensitive))

		await super().send_packet(message)

	async def handle_bridges(self, message: Post):
		fetch = False
		if isinstance(message.user, User):
			fetch = True

		if message.user.username in self.__bridges__ and ":" in message.data:
			split = message.data.split(":", 1)
			message.data = split[1].strip()
			message.user = PartialUser(split[0].strip(), self)
			if fetch:
				data = self.cache.get_user(message.user.username)
				if not isinstance(data, User):
					data = await message.user.fetch()

				if data:
					message.user = data

		if message.data.startswith(self.prefix + "#0000"):
			message.data = message.data.replace("#0000", "")

		return message

	def get_context(self, message: Post):
		return Context(message, self)

	async def run_commands(self, message: Post):

		args = shlex.split(str(message))

		if (err := await self.commands[args[0]].run_cmd(
				self.get_context(message), *args[1:]
		)) is not None:

			await self._run_event(CallBackIds.error, err)
			return err

	def command(self, name=None, args=0, aliases: Optional[List[str]] = None): # type: ignore
		def inner(func):

			cmd = AppCommand(func, name=name, args=args, alias=aliases)

			self.commands = AppCommand.add_command(self.commands, cmd)

			return cmd
		return inner

	async def _connect(self):
		await self._send_initial_commands()
		packet = await self._authenticate()
		await self._process_login_response(packet)

	async def _send_initial_commands(self):
		await self.send_packet({"cmd": "direct", "val": "meower", "listener": "send_tkey"})
		await self.send_packet({"cmd": "direct", "val": {"cmd": "type", "val": "py"}})

	async def _authenticate(self):
		async with self.packet_condition:
			await self.send_packet({
				"cmd": "direct",
				"val": {
					"cmd": "authpswd",
					"val": {
						"username": str(self.username).strip(),
						"pswd": str(self.password).strip()
					}
				},
				"listener": "mb.py_login"
			})

			while True:
				await self.packet_condition.wait()

				if self._packets[-1].get("listener") != "mb.py_login":
					continue

				if self._packets[-1]["cmd"] == "statuscode" and self._packets[-1]["val"] != "I: 100 | OK":
					raise Exception(f"Wrong Username or Password!\n {self._packets[-1]['val']}")
				elif self._packets[-1]["cmd"] == "statuscode":
					self._packets.pop(-1)
					continue

				if not (self._packets[-1]["cmd"] == "direct" and "payload" in self._packets[-1]["val"].keys()):
					continue

				return self._packets.pop(-1)

	async def _process_login_response(self, packet):
		await self.api.login(packet['val']['payload']['token'])
		self.user = await self.user.fetch()

		if self.api.base_uri.startswith("https://api.meower.org"):
			key = secrets.token_urlsafe()

			chat = self.get_chat((await self.api.users.dm("Utils"))[0]._id)
			await chat.send_msg(key)

			httpx.put(f"https://meower-utils.showierdata.xyz/bot/{self.user.name}", json={
				"key": key,
				"library": "MeowerBot.py"
			})

		await self._run_event(CallBackIds.login, packet['val']['payload']['token'])

	def register_cog(self, cog: Cog):
		self.cogs[cog.__class__.__name__] = cog

		self.update_commands()

	async def _disconnect(self):

		await self._run_event(CallBackIds.disconnect)

	def get_chat(self, chat_id: str):
		chat = self.cache.get_chat(UUID(chat_id))
		if chat is None:
			return PartialChat(chat_id, self)
		return chat

	async def _message(self, message: dict):
		# noinspection PyBroadException
		try:
			if message.get("cmd") == "direct" and message.get("listener") == 'mb.py_login':
				message_sensitive = copy.deepcopy(message)
				message_sensitive['val']['payload']['token'] = "<TOKEN>"
				self.logger.debug(f"Recived message: {message_sensitive}")
			else:
				self.logger.debug(f"Recived message: {message}")
		except Exception:
			pass

		match message["cmd"]:
			case "statuscode":
				return await self._run_event(CallBackIds.statuscode, message["val"], message.get("listener"))

			case "ulist":
				usernames = message["val"].split(";")
				usernames.pop()
				self.userlist = []
				for user in usernames:

					if userobj := self.cache.get_user(user):
						self.userlist.append(user)
						continue
					user = await PartialUser(user, self).fetch()
					self.userlist.append(user)
					self.cache.add_user(user)

				await self._check_bot_users(usernames)
				return await self._run_event(CallBackIds.ulist, self.userlist)

			case "direct":
				await self._handle_direct(message)

	async def _handle_direct(self, message):
		await self._run_event(CallBackIds.direct, message)

		if "post_origin" not in message["val"]:
			return

		await self._run_event(CallBackIds.raw_message, message["val"]) # type: ignore[call-arg]
		post = Post(self, message["val"], chat=message["val"]["post_origin"])
		async with self.post_condition:
			self.messages.append(post)
			self.post_condition.notify_all()
			self.messages = self.messages[0: 50]

		await self._run_event(CallBackIds.message, post)

	async def _check_user(self, user):
		if self.cache.bots.get(user): return

		resp = httpx.get(f"https://meower-utils.showierdata.xyz/bots/{user}")
		if resp.status_code != 200:
			return

		self.cache.add_bot(user, resp.json())

	async def _check_bot_users(self, userlist):
		assert self.api is not None
		if not self.api.headers.get("token"):
			return

		# noinspection PyUnusedLocal
		loop = asyncio.get_event_loop()

		self.cache.try_clear_bots()

		# NO ONE CARES FOR CREATE_TASK DAMMIT PYCHARM
		# noinspection PyAsyncCall
		asyncio.gather(*[self._check_user(username) for username in userlist])

	async def _error(self, error):

		await self._run_event(CallBackIds.error, error)

	async def start(self, username, password, server="wss://server.meower.org", ):
		"""
		Runs The bot (Blocking)
		"""
		self.username = username
		self.password = password
		self.user = PartialUser(self.username, self)
		self.update_commands()
		# noinspection PyAsyncCall
		asyncio.create_task(self._t_ping())
		if self.prefix is None:
			self.prefix = "@" + self.username
		self.logger = logging.getLogger(f"MeowerBot {self.username}")
		self.server = server

		self.api = MeowerAPI(username=username)

		await self.connect(server)

	def run(self, username, password, server="wss://server.meower.org", ):
		"""
			Runs the bot  (Blocking)
		"""
		loop = asyncio.get_event_loop()
		fut = loop.create_task(self.start(username, password, server=server))
		loop.run_forever()

		return fut


__all__ = ["Bot", "CallBackIds", 'cbids']
