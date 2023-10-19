import shlex

from .cl import Client
import sys

import json
import traceback

import requests


import time

from .command import AppCommand
from .context import Context, Post, PartialUser, User

import time
import logging

from .API import MeowerAPI

import asyncio
import sys

from enum import StrEnum

from typing import Union

class cbids(StrEnum):
		error = "error"
		__raw__ = "__raw__"
		login = "login"
		close = "close"
		ulist = "ulist"
		message = "message"
		raw_message = "raw_message"
		direct = "direct"

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
				self.logger.error(e)
				await self._error(e)
				break

	def __init__(self, prefix=None ): #type: ignore
		super().__init__()
		self.callbacks = {i: [] for i in callbacks}
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
	

	def subcommand(self, name=None, args=0, aliases = None):
		def inner(func):

			cmd = AppCommand(func, name=name, args=args)
			cmd.register_class(self.connected)

			self.commands = AppCommand.add_command(self.commands, cmd)


			return cmd #dont want mb to register this as a root command
		return inner

	def update_commands():
		for cog in self.cogs:
			cog.update_commands()

			self.commands = self.commands.update(cog.__commands__)

	async def error(self, err: Exception): pass
	async def __raw__(self, packet: dict): pass
	async def login(self, token: str): pass 
	async def close(self): pass
	async def ulist(self, ulist): pass

	async def message(self, message: Post): 
		message = self.handle_bridges(message)
	

	async def raw_message(self, data: dict): pass
	async def direct(self, data: dict): pass

	
	async def _run_event(self, event: cbids, *args, **kwargs):
		err = await asyncio.gather(*([getattr(self, event)] + self.callbacks[event]), return_exceptions=True)
		for i in err:
			if isinstance(i, Exception):
				await self._error(i)


	# websocket
	
	def handle_bridges(self, message: Post):
		fetch = False
		if isinstance(message.user, User):
			fetch = True

		if message.user.name in self.__bridges__ and ":" in message.data:
			split = message.data.split(": ", 1)
			message.data = split[1]
			message.user = PartialUser(split[0], self)
			if fetch:
				message.user = await message.user.fetch()
		
		

		if message.data.startswith(self.prefix + "#0000"):
			message.data = message.data.replace("#0000", "")
			
		return packet



	async def _connect(self):
		await self.sendPacket({"cmd": "direct", "val": {
			"cmd": "type", "val": "MeowerBot.py"
		}})

		if (await self.send_statuscode_request({ "cmd": "direct", val: "meower", "listener": "send_tkey" }))["val"] != "I: 100 | OK":
			raise RuntimeError("Meower Trust Failed!")
		
		resp = await self.send_data_request(
			{
  				"cmd": "direct",
  				"val": {
				    "cmd": "authpswd",
				    "val": {
				      "username": self.username,
				      "pswd": self.password
				    }
			  }
		   }
		)	
	
		if resp[1]["val"] != "I: 100 | OK":
			raise Exception(f"Wrong Username or Password!\n {resp[1]['val']}")

		self.api.login(resp[0]["val"["val"]["pswd"]])

		await self._run_event(cbids.login, resp[0]["val"]["pswd"])

	


	async def _disconnect(self):
		await self._run_event(cbids.close)

	async def _message(self, message):
		pass

	async def _error(self, error):
		pass

	async def run(self, username, password, server="wss://server.meower.org"):
		"""
		Runs The bot (Blocking)
		"""
		self.username = username
		self._password = password

		asyncio.create_task(self._t_ping())
		if self.prefix is None:
			self.prefix = "@" + self.username
		self.logger = logging.getLogger(f"MeowerBot {self.username}")
		self.server = server
		
		self.api = MeowerAPI(username=username)
	
			
		await self.connect(server)
		
