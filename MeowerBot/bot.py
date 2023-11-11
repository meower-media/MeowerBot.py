from __future__ import annotations
import shlex
from .cl import Client
import traceback
from .command import AppCommand
from .context import Context, Post, PartialUser, User, PartialChat
import logging
from .api import MeowerAPI
import asyncio
from enum import StrEnum
from .cog import Cog
from typing import Dict, Callable


class cbids(StrEnum):
	"""Callbacks that the bot calls. You can find more documentation in :class:`MeowerBot.bot.Bot`"""
	error = "error"
	__raw__ = "__raw__"
	login = "login"
	close = "close"
	ulist = "ulist"
	message = "message"
	raw_message = "raw_message"
	direct = "direct"
	statuscode = "statuscode"

callbacks = [i for i in cbids] # type: ignore


class Bot(Client):
	"""A class that holds all of the networking for a meower bot to function and run"""

	messages: list[Post] = [] #: :meta private: :meta hide-value:
	message_condition = asyncio.Condition() #: :meta private: :meta hide-value:

	__bridges__ = [ #: :meta public: :meta hide-value:
			"Discord",
			"Revower",
			"revolt"
	]


	BOT_NO_PMSG_RESPONSE = [ #: :meta private: :meta hide-value:
		"I:500 | Bot",
		"I: 500 | Bot"
	]

	userlist: list[str] = None #: :meta hide-value:

	@property
	def latency(self) -> int:
		"""Gets the latency of the bot

		:return: Bot latency
		:rtype: int
		"""
		return self.ws.latency

	async def _t_ping(self):
		while True:
			try:
				await asyncio.sleep(5)

				await self.sendPacket({"cmd": "ping", "val": ""})
				self.logger.debug(msg="Sent ping")
			except Exception as e:
				await self._error(e)
				break

	def __init__(self, prefix=None): # type: ignore

		super().__init__()
		self.callbacks: Dict[str, list[Callable]] = {str(i): [] for i in callbacks}
		self.callbacks["__raw__"] = []
		self.userlist = []

		# to be used in start
		self.username: str = None #: :meta hide-value:
		self.password: str = None #: :meta hide-value:

		self.commands = {}
		self.prefix = prefix
		self.logger = logging.getLogger("MeowerBot")
		self.server: str = None

		self.cogs: Dict[str, Cog] = {}
	# Interface

	def event(self, func: Callable):
		"""Creates a callback that takes over the original functionality of the bot.

		valid callbacks are defined in :class:`cbids`

		:param func: The function that
		:type func: Callable
		:raises TypeError: The func provided does not have a valid callback name
		"""
		if func.__name__ not in callbacks:
			raise TypeError(f"{func.__name__} is not a valid callback")

		setattr(self, func.__name__, func)

	def listen(self, callback: str = None):
		"""
		Does the same thing as :meth MeowerBot.bot.Bot.event:but does not replace the bots original functionality

		valid callbacks are defined in :class:`cbids`
		:raises TypeError: The listener provided is not valid
		"""
		def inner(func):
			nonlocal callback
			callback = callback if callback is not None else func.__name__

			if func.__name__ not in callbacks:
				raise TypeError(f"{func.__name__} is not a valid listener")

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

	async def __raw__(self, packet: dict):
		"""Callback for raw packets. Gets called before the bot does any processing.

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		pass

	async def login(self, token: str):
		"""Gets called when the bot is fully ready and logged into meower

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		pass

	async def close(self):
		"""Gets called when the bot get disconnected from meower

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		pass

	async def ulist(self, ulist: list[str]):
		"""Gets called when a user connects to meower.

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		pass

	async def message(self, message: Post):
		"""Method for overiding how the bot handles messages.

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		message = await self.handle_bridges(message)

		if not message.data.startswith(self.prefix):
			return

		message.data = message.data.removeprefix(self.prefix)

		await self.run_commands(message)

	async def statuscode(self, status, listerner): pass
	async def raw_message(self, data: dict): pass
	async def direct(self, data: dict): pass


	async def _run_event(self, event: cbids, *args, **kwargs):
		events = [getattr(self, str(event))]
		for i in self.callbacks[str(event)]:
			if type(i) is list:
				events.extend(i)
			elif callable(i):  # Check if the element is Callable
				events.append(i)

		err = await asyncio.gather(*[i(*args, **kwargs) for i in events if callable(i)], return_exceptions=True)
		for i in err:
			if i is not None:
				if isinstance(i, Exception) and event != cbids.error:
					await self._error(i)

	# websocket

	async def handle_bridges(self, message: Post):
		fetch = False
		if isinstance(message.user, User):
			fetch = True

		if message.user.username in self.__bridges__ and ":" in message.data:
			split = message.data.split(":", 1)
			message.data = split[1].strip()
			message.user = PartialUser(split[0].strip(), self)
			if fetch:
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

			await self._run_event(cbids.error, err)


	def command(self, name=None, args=0, aliases: list[str] = None):
		def inner(func):

			cmd = AppCommand(func, name=name, args=args)

			self.commands = AppCommand.add_command(self.commands, cmd)


			return cmd
		return inner


	async def _connect(self):
		await self._send_initial_commands()
		await self._authenticate()
		await self._process_login_response()

	async def _send_initial_commands(self):
		await self.sendPacket({"cmd": "direct", "val": "meower", "listener": "send_tkey"})
		await self.sendPacket({"cmd": "direct", "val": {"cmd": "type", "val": "py"}})

	async def _authenticate(self):
		async with self.message_condition:
			await self.sendPacket({
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
				await self.message_condition.wait()

				if self._packets[-1].get("listener") != "mb.py_login":
					continue

				if self._packets[-1]["cmd"] == "statuscode" and self._packets[-1]["val"] != "I: 100 | OK":
					raise Exception(f"Wrong Username or Password!\n {self._packets[-1]['val']}")

				if not (self._packets[-1]["cmd"] == "direct" and "payload" in self._packets[-1]["val"].keys()):
					continue

				break


	async def _process_login_response(self):
		await self.api.login(self._packets[-1]['val']['payload']['token'])
		await self._run_event(cbids.login, self._packets[-1]['val']['payload']['token'])

	def register_cog(self, cog: Cog):
		self.cogs[cog.__class__.__name__] = cog

		self.update_commands()

	async def _disconnect(self):

		await self._run_event(cbids.close)

	def get_chat(self, id):
		return PartialChat(id, self)

	async def _message(self, message: dict):
		if (message.get("listener")) != "mb.py_login":
			self.logger.debug(message)
		match message["cmd"]:
			case "statuscode":
				return await self._run_event(cbids.statuscode, message["val"], message.get("listener"))

			case "ulist":
				self.ulist = message["val"].split(";")

				return await self._run_event(cbids.ulist, self.ulist)

			case "direct":
				if "post_origin" in message["val"]: # post
					await self._run_event(cbids.__raw__, message["val"])
					post = Post(self, message["val"], chat=message["val"]["post_origin"])
					async with self.message_condition:
						self.messages.append(post)
						self.message_condition.notify_all()
						self.messages = self.messages[0: 50]

					await self._run_event(cbids.message, post)
				else:
					return await self._run_event(cbids.direct, message)


		if (message["cmd"] == "pmsg") and (message["val"] not in self.BOT_NO_PMSG_RESPONSE):
			self.wss.sendPacket({
					"cmd": "pmsg",
					"val": "I:500 | Bot",
					"id": message["origin"]
			})






	async def _error(self, error):

		await self._run_event(cbids.error, error)


	async def start(self, username, password, server="wss://server.meower.org", ):
		"""
		Runs The bot (Blocking)
		"""
		self.username = username
		self.password = password
		self.update_commands()
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


__all__ = ["Bot", "cbids"]
