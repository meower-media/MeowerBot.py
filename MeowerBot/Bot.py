import shlex

from .cl import Client
import sys

import json
import traceback

import requests


import time

from .command import AppCommand
from .context import CTX

import time
import logging

from .API import MeowerAPI

import asyncio
import sys

if sys.version_info >= (3, 11):
	from enum import StrEnum
else:
	from backports.strenum import StrEnum

from typing import Union

class cbids(StrEnum):
		error = "error"
		__raw__ = "__raw__"
		login = "login"
		close = "close"
		statuscode = "statuscode"
		ulist = "ulist"
		message = "message"
		raw_message = "raw_message"
		chat_list = "chat_list"
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
	

	

	




	# websocket

	async def _connect(self):
		pass

	async def _disconnect(self):
		pass

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
		try:
			self.api = MeowerAPI(username=username)
		except: # nosec
			pass
		await self.connect(server)
		
