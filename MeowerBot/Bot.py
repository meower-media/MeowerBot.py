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

class Bot(Client):
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
			await asyncio.sleep(30)

			await self.sendPacket({"cmd": "ping", "val": ""})

	def __init__(self, prefix=None ): #type: ignore
		super().__init__()
		self.callbacks = {}
		self._last_to = "Home"
		self.ulist = []

		# to be used in start
		self.username = None
		self.password = None
		self.logger_in = False

		self.commands = {}
		self.prefix = prefix
		self.logger = logging.getLogger("MeowerBot")
		self.bad_exit = False
		self.server = None

		self.cogs = {}

	async def run_cb(self, cbid, args=(), kwargs=None):  # cq: ignore
		if cbid not in self.callbacks:
			return  # ignore

		if not kwargs:
			kwargs = {}
		
		if cbid == "error" and isinstance(args[0], KeyboardInterrupt()): 
			self.logger.error("KeyboardInterrupt")
			self.bad_exit = True
			self.stop()
			return 

		kwargs["bot"] = self
		await asyncio.gather(*[cb(*args, **kwargs) for cb in self.callbacks[cbid]])

	async def _error(self, e):
		await self.run_cb("error", args=(e,))

		if (type(e)) == KeyboardInterrupt:
			self.bad_exit = True

		self.wss = None # effectively kill the bot

	async def _message(self, packet):
		
		try:
			await self.__handle_packet__(packet)
		except BaseException as e:  # cq: skip #IDC ABOUT GENERAL EXCP
			self.logger.error(traceback.format_exc())
			await self.run_cb("error", args=(e, ))


		try:
			await self.run_cb("__raw__", args=(packet, ))  # raw packets
		except BaseException as e:  # cq: skip #IDC ABOUT GENERAL EXCP
			self.logger.error(traceback.format_exc())
			await self.run_cb("error", args=(e, ))

	async def _connect(self):
		await self.sendPacket(
			{
				"cmd": "direct",
				"val": {"cmd": "type", "val": "py"},
			}
		)
		await self.sendPacket(
			{
				"cmd": "direct",
				"val": "meower",
				"listener": "__meowerbot__cloudlink_trust",
			}
		)

	def command(self, aname=None, args=0):
		def inner(func):
			if aname is None:
				name = func.__name__
			else:
				name = aname

			cmd = AppCommand(func, name=name, args=args)

			info = cmd.info()
			info[cmd.name]["command"] = cmd

			self.commands.update(info)

			return cmd #allow subcommands without a cog

		return inner

	def register_cog(self, cog):
		info = cog.get_info()
		self.cogs[cog.__class__.__name__] = cog
		self.commands.update(info)

	def deregister_cog(self, cogname):
		for cmd in self.cogs[cogname].get_info().values():
			del self.commands[cmd.name]
		del self.cogs[cogname]

	async def _handle_status(self, status, listener):
		if status == "I:112 | Trusted Access enabled":
			return

		if self.logger_in:
			self.logger_in = False

			if status != "I:100 | OK":
				raise RuntimeError("CloudLink Trust Failed")

			auth_packet = {
				"cmd": "direct",
				"val": {
					"cmd": "authpswd",
					"val": {"username": self.username, "pswd": self._password},
				},
				"listener": "__meowerbot__login",
			}
			await self.sendPacket(auth_packet)

		elif listener == "__meowerbot__login":
			if status == "E:104 | Internal":
				requests.post(
					"https://webhooks.meower.org/post/home",
					json={
						"post": "ERROR: MeowerBot.py Webhooks Logging\n\n Account Softlocked.",
						"username": self.username,
					},
					timeout=5
				)
				print("CRITICAL ERROR! ACCOUNT SOFTLOCKED!!!!.", file=sys.__stdout__)
				self.bad_exit = True
				return

			if status != "I:100 | OK":
				raise RuntimeError("Password Or Username Is Incorrect")

			time.sleep(0.5)
			await self.run_cb("login", args=(), kwargs={})

		elif listener == "__meowerbot__send_message":
			if status == "I:100 | OK":
				return

			raise RuntimeError("Post Failed to send")

	def callback(self, callback, cbid: Union[Union[cbids,  None], str] =None):
		"""Connects a callback ID to a callback
		"""
		if cbid is None:
			cbid = callback.__name__

		if cbid not in self.callbacks:
			self.callbacks[cbid] = []
		self.callbacks[cbid].append(callback)

	async def _close(self, *args, **kwargs):
		await self.run_cb("close", args=args, kwargs=kwargs)

	def handle_bridges(self, packet):
		if packet["val"]["u"] in self.__bridges__ and ": " in packet["val"]["p"]:
				split = packet["val"]["p"].split(": ", 1)
				packet["val"]["p"] = split[1]
				packet["val"]["u"] = split[0]
		
		if packet["val"]["p"].startswith(self.prefix+"#0000"):
			packet["val"]["p"] = packet["val"]["p"].replace("#0000", "")
		
		return packet

	async def __handle_packet__(self, packet):
		if packet["cmd"] == "statuscode":

			await self._handle_status(packet["val"], packet.get("listener", None))

			listener = packet.get("listener", None)
			return await self.run_cb("statuscode", args=(packet["val"], listener))

		elif packet["cmd"] == "ulist":
			self.ulist = packet["val"].split(";")
			await self.run_cb("ulist", self.ulist)

		elif packet["cmd"] == "direct" and "post_origin" in packet["val"]:
			packet = self.handle_bridges(packet)

			ctx = CTX(packet["val"], self)
			if "message" in self.callbacks:
				await self.run_cb("message", args=(ctx.message,))

			else:

				if ctx.user.username == self.username:
					return
				if not ctx.message.data.startswith(self.prefix):
					return

				ctx.message.data = ctx.message.data.split(self.prefix, 1)[1]

				await self.run_command(ctx.message)

			await self.run_cb("raw_message", args=(packet["val"],))

		elif packet["cmd"] == "direct":
			listener = packet.get("listener")

			if listener == "mb_get_chat_list":
				await self.run_cb("chat_list", args=(packet["val"]["payload"], listener))
			elif listener == "__meowerbot__login":
				self.api.login(packet['val']['payload']['token'])
			await self.run_cb("direct", args=(packet["val"], listener))

		

		else:
			listener = packet.get("listener")
			await self.run_cb(packet["cmd"], args=(packet["val"], listener))

		
		if (packet["cmd"] == "pmsg") and  (packet["val"] not in self.BOT_NO_PMSG_RESPONSE):
			await self.sendPacket({
				"cmd": "pmsg",
				"val": "I:500 | Bot",
				"id": packet["origin"]
			})

	async def run_command(self, message):
		args = shlex.split(str(message))

		try:
			await self.commands[args[0]]["command"].run_cmd(message.ctx, *args[1:])
		except KeyError as e:
			self.logger.error(traceback.format_exc())
			await self.run_cb("error", args=(e,))

	async def send_msg(self, msg, to="home"):
		self._last_to = to
		self._last_sent = msg
		
		if to == "home":
			await self.sendPacket(
				{
					"cmd": "direct",
					"val": {"cmd": "post_home", "val": msg},
					"listener": "__meowerbot__send_message",
				}
			)
		else:
			await self.sendPacket(
				{
					"cmd": "direct",
					"val": {"cmd": "post_chat", "val": {"chatid": to, "p": msg}},
					"listener": "__meowerbot__send_message",
				}
			)
	

	async def send_typing(self, to="home"):
		if  to == "home":
			await self.sendPacket(
				{
					"cmd": "direct",
					"val": {
						"cmd": "set_chat_state",
						"val": {
							"chatid": "livechat",
							"state": 101,
						},
					},
				}
			)
		else:
		  await self.sendPacket(
			{
				"cmd": "direct",
				"val": {
					"cmd": "set_chat_state",
					"val": {
						"chatid": to,
						"state": 100,
					},
				},
			}
		  )
		
	async def enter_chat(self, chatid="livechat"):
		await self.sendPacket(
			{
				"cmd": "direct",
				"val": {
					"cmd": "set_chat_state",
					"val": {
						"chatid": chatid,
						"state": 1,
					},
				},
			}
		)

	async def create_chat(self, name):
		"""
		Unstable, use at your own risk

		comes with callbacks: chat_list 
		"""
		await self.sendPacket({
			"cmd": "direct",
			"val": {
				"cmd": "create_chat",
				"val": name
			},
			"listener": "mb_create_chat"
		})

		time.sleep(secs=0.5)

		await self.sendPacket({
			"cmd": "direct",
			"val": {
				"cmd": "get_chat_list",
				"val": {
					"page": 1
				}
			},
			"listener": "mb_get_chat_list"
		})

	async def run(self, username, password, server="wss://server.meower.org"):
		"""
		Runs The bot (Blocking)
		"""
		self.username = username
		self._password = password
		self.logger_in = True

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
		
		if self.bad_exit:
			raise BaseException("Bot Account Softlocked")
