from typing import List

from MeowerBot.context import Post


class Events:
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

	async def disconnect(self):
		"""Gets called when the bot gets disconnected from meower

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		pass

	async def ulist(self, ulist: List[str]):
		"""Gets called when a user connects to meower.

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		pass

	async def statuscode(self, status, listerner): pass

	async def raw_message(self, data: dict): pass

	async def direct(self, data: dict): pass

	async def error(self, err: Exception):
		"""Handles errors for the bot.

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		pass

	async def message(self, message: Post):
		"""Method for overiding how the bot handles messages.

		This is a callback for :meth:`MeowerBot.bot.Bot.event`
		"""
		pass