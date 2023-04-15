from datetime import datetime

import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Bot import Bot

import weakref
import requests


class User:
    def __init__(self, bot, username):
        self.username = username
        
        self.bot = bot
        self._raw = self.bot.api.get_user(self.username)

        self.level = self._raw["lvl"]
        self.pfp = self._raw["pfp_data"]
        self.quote = self._raw["quote"]

    

    def ping(self, msg, to="home"):
        self.bot.send_msg(f"@{self.username} {msg}", to=to)

    def __str__(self):
        return str(self.__dict__)


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

    def send_msg(self, msg):
        self.bot.send_msg(msg, to=self.message.chat)

    def reply(self, msg):
        self.user.ping(msg, to=self.message.chat)
