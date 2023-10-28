import shlex
from .cl import Client
import traceback
from .command import AppCommand
from .context import Context, Post, PartialUser, User, PartialChat
import logging
from .API import MeowerAPI
import asyncio
from enum import StrEnum
from .cog import Cog
class cbids(StrEnum):
		error = "error"
		__raw__ = "__raw__"
		login = "login"
		close = "close"
		ulist = "ulist"
		message = "message"
		raw_message = "raw_message"
		direct = "direct"
		statuscode = "statuscode"

callbacks = [i for i in cbids]

class Bot(Client):
	messages = []
	message_condition = asyncio.Condition()

	
	"""
	A class that holds all of the networking for a meower bot to function and run
	"""
	__bridges__ = [
			"Discord",
			"Revower",
			"revolt"
		]
	


	BOT_NO_PMSG_RESPONSE = [
		"I:500 | Bot",
		"I: 500 | Bot"
	]
	ulist = None

	@property
	def latency(self):
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

	def __init__(self, prefix=None): #type: ignore
		super().__init__()
		self.callbacks = {str(i): [] for i in callbacks}
		self.callbacks["__raw__"] = []
		self.ulist = []

		# to be used in start
		self.username = None
		self.password = None

		self.commands = {}
		self.prefix = prefix
		self.logger = logging.getLogger("MeowerBot")
		self.server = None

		self.cogs = {}
	# Interface

	def event(self, func):
		"""
		Creates a callback that takes over the original functionality of the bot.
		throws an error if the function name is not a valid callback

		throws:
			- TypeError
		
		"""
		if func.__name__ not in callbacks:
			raise TypeError(f"{func.__name__} is not a valid callback")
		
		setattr(self, func.__name__, func)
	
	def listen(self, callback=None):
		"""
		Does the same thing as @link Bot.event but does not replace the bots original functionality, most usefull for librarys
		throws an error if the function name is not a valid callback

		throws:
			- TypeError
		"""
		def inner(func):
			callback = callback if callback is not None else func.__name__

			if func.__name__ not in callbacks:
				raise TypeError(f"{func.__name__} is not a valid listener")
		
			self.callbacks[callback].append(func)

			return func
		return inner
	

	def subcommand(self, name=None, args=0, aliases = None):
		def inner(func):

			cmd = AppCommand(func, name=name, args=args)
			cmd.register_class(self.connected)

			self.commands = AppCommand.add_command(self.commands, cmd)


			return cmd #dont want mb to register this as a root command
		return inner

	def update_commands(self):
		for cog in self.cogs.values():
			cog.update_commands()

			self.commands.update(cog.commands)
			for i in cog.callbacks.keys():
				self.callbacks[str(i)].append(cog.callbacks[str(i)])


	async def error(self, err: Exception): 
		self.logger.error(traceback.print_exception(err))

	async def __raw__(self, packet: dict): pass
	async def login(self, token: str): pass 
	async def close(self): pass
	async def ulist(self, ulist): pass

	async def message(self, message: Post): 
		message = await self.handle_bridges(message)

		if not message.data.startswith(self.prefix):
			return
		
		message.data = message.data.removeprefix(self.prefix)

		await self.run_commands(message)

	async def statuscode(self, status, listerner):
		pass

	async def raw_message(self, data: dict): pass
	async def direct(self, data: dict): pass

	
	async def _run_event(self, event: cbids, *args, **kwargs):
		events = [getattr(self, str(event))]
		for i in self.callbacks[str(event)]:
			if type(i) is list:
				events.extend(i)
			elif callable(i):  # Check if the element is callable
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
			split = message.data.split(": ", 1)
			message.data = split[1]
			message.user = PartialUser(split[0], self)
			if fetch:
				message.user = await message.user.fetch()
		
		

		if message.data.startswith(self.prefix + "#0000"):
			message.data = message.data.replace("#0000", "")
			
		return message
	
	def get_context(self, message: Post):
		return Context(message, self)

	async def run_commands(self, message: Post):

		args = shlex.split(str(message))

		try:
			await self.commands[args[0]].run_cmd(self.get_context(message), *args[1:])
		except Exception as e:
			await self._error(e)

	def command(self, name=None, args=0, aliases = None):
		def inner(func):

			cmd = AppCommand(func, name=name, args=args)

			self.commands = AppCommand.add_command(self.commands, cmd)
					

			return cmd 
		return inner
	


	async def _connect(self):
		await self.sendPacket({ "cmd": "direct", "val": "meower", "listener": "send_tkey" })
		
		await self.sendPacket({"cmd": "direct", "val": {
			"cmd": "type", "val": "py"
		}})


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
					raise Exception(f"Wrong Username or Password!\n {self._packets[-1]["val"]}")

				if not (self._packets[-1]["cmd"] == "direct" and "payload" in self._packets[-1]["val"].keys()):
					continue

				break
 
			await self.api.login(self._packets[-1]['val']['payload']['token'])

			await self._run_event(cbids.login, self._packets[-1]['val']['payload']['token'])

	

	def register_cog(self, cog: Cog):
		self.cogs[cog.__class__.__name__] = cog

		self.update_commands()

	async def _disconnect(self):
		
		await self._run_event(cbids.close)

	def get_chat(self, id):
		return PartialChat(id, self)

	async def _message(self, message):
		if (message.get("listener")) != "mb_login":
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
					
					await self._run_event(cbids.message, post)
				else:
					return await self._run_event(cbids.direct, message)
				

        
		if (message["cmd"] == "pmsg") and  (message["val"] not in self.BOT_NO_PMSG_RESPONSE):
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
		fut = loop.create_task( self.start(username, password, server=server) )
		loop.run_forever()



