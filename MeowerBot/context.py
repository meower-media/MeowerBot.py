from datetime import datetime

import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Bot import Bot

import weakref
import requests



class Chat:
    def __init__(self, id, display_name, bot: "Bot"):
        self.id = id
        self.display_name = display_name
        self.bot: "Bot" = bot

    async def send_msg(self, message):
        self.bot.api.send_post(self.id, message)


class Post:
    def __init__(self, bot, _raw):
        self.bot = bot
        self._raw = _raw
        self.user = User(bot, self._raw["u"])

        self.chat = self._raw["post_origin"]
        self.data = self._raw["p"]
        self._id = self._raw["post_id"]
        self.type = self._raw["type"]
        self.date = datetime.fromtimestamp(self._raw["t"]["e"])
        self.ctx: CTX = None  # type: ignore

    def __str__(self):
        return str(self.data)


class CTX:
    def __init__(self, post, bot):
        self.message = Post(bot, post)
        self.user = self.message.user
        self.bot = bot
        self.message.ctx = weakref.proxy(self)  # type: ignore

    async def send_msg(self, msg):
        await self.bot.send_msg(msg, to=self.message.chat)

    async def reply(self, msg):
        await self.user.ping(msg, to=self.message.chat)
