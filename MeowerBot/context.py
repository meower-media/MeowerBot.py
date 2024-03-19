from datetime import datetime
from typing import Optional, TYPE_CHECKING

from .api.shared import api_resp
from .data.api.chats import ChatGroup
from .data.api.user import User as RawUser

if TYPE_CHECKING:
	from . import Bot


class PartialChat:
	def __init__(self, id, bot):
		self.id = id
		self.bot = bot

	async def send_msg(self, message) -> Optional["Post"]:
		data, status = await self.bot.api.send_post(self.id, message)

		if status != 200:
			return None
		return Post(self.bot, data.to_dict(), self)

	async def fetch(self) -> Optional["Chat"]:
		chat = self.bot.cache.get_chat(self.id)
		if isinstance(chat, Chat): return chat

		data, status = await self.bot.api.chats.get(self.id)

		if status != 200:
			return None

		chat = Chat(data, self.bot)
		self.bot.cache.add_chat(chat)
		return chat


class Chat(PartialChat):
	def __init__(self, data: ChatGroup, bot):
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
	def __init__(self, username: str, bot):
		self.username: str = username
		self._bot: "Bot" = bot
		self.bot: bool = username in self._bot.cache.bots

	async def fetch(self) -> Optional["User"]:
		user = self._bot.cache.get_user(self.username)
		if isinstance(user, User): return user

		data, status = api_resp(RawUser, await self._bot.api.users._get(self.username, "", None))

		user = User(self.username, self._bot, data) if status == 200 else None
		self._bot.cache.add_user(user)
		return user


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
	def __init__(self, bot, _raw: dict, chat):
		self._bot = bot
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
		await self.chat.send_msg(f"@{self.user.username} [{self._id}] {message}")


class Context:
	def __init__(self, post: Post, bot):
		self.message = post
		self.user = self.message.user
		self._bot = bot

	async def send_msg(self, msg):
		return await self.message.chat.send_msg(msg)

	async def reply(self, msg):
		await self.message.reply(msg)
