from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from .bot import Bot

from .data.api.chats import ChatGroup
from .data.api.user import User as RawUser
from .api.shared import api_resp

from typing import Optional


class PartialChat:
	def __init__(self, id, bot: "Bot"):
		self.id = id
		self.bot: "Bot" = bot

	async def send_msg(self, message) -> Optional["Post"]:
		data, status = await self.bot.api.send_post(self.id, message)

		if status != 200:
			return None
		return Post(self.bot, data.to_dict(), self)

	async def fetch(self) -> Optional["Chat"]:
		data, status = await self.bot.api.chats.get(self.id)

		if status != 200:
			return None

		return Chat(data, self.bot)


class Chat(PartialChat):
	def __init__(self, data: ChatGroup, bot: "Bot"):
		super().__init__(data._id, bot)

		self.created	 = data.created
		self.deleted	 = data.deleted
		self.last_active = data.last_active
		self.members	 = data.members

		self.owner	   = data.owner
		self.type		= data.type
		self.nickname	= data.nickname
		self.data		= data


class PartialUser:
	def __init__(self, username: str, bot: "Bot"):
		self.username: str = username
		self.bot = bot

	async def fetch(self) -> Optional["User"]:
		data, status = api_resp(RawUser, await self.bot.api.users._get(self.username, ""))

		assert type(data) is RawUser

		return User(self.username, self.bot, data) if status == 200 else None


class User(PartialUser):
	def __init__(self, username, bot, data: RawUser):
		super().__init__(username, bot)

		self.data: RawUser = data

		self.banned                 = self.data.banned
		self.created			    = self.data.created
		self.flags			        = self.data.flags
		self.last_seen		        = self.data.last_seen
		self.data.lower_username    = self.data.lower_username
		self.lvl				    = self.data.lvl
		self.name				    = self.data.name
		self.permissions		    = self.data.permissions
		self.pfp_data			    = self.data.pfp_data
		self.quote			        = self.data.quote
		self.id				        = self.data.uuid


class Post:
	def __init__(self, bot: "Bot", _raw: dict, chat):
		self.bot = bot
		self._raw = _raw
		self.user: PartialUser | User = PartialUser(self._raw["u"], bot)

		self.chat: PartialChat = PartialChat(chat, bot)
		self.data: str  = self._raw["p"]
		self._id = self._raw["post_id"]
		self.type = self._raw["type"]
		self.date = datetime.fromtimestamp(self._raw["t"]["e"])

	def __str__(self):
		return str(self.data)

	async def reply(self, message):
		self.chat.send_msg(f"@{self.user.username} [{self.id}] {message}")


class Context:
	def __init__(self, post: Post, bot):
		self.message = post
		self.user = self.message.user
		self.bot = bot

	async def send_msg(self, msg):
		await self.message.chat.send_msg(msg)

	async def reply(self, msg):
		await self.message.reply(msg)
