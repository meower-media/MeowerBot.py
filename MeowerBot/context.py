from datetime import datetime
from typing import Literal, Optional, TYPE_CHECKING, cast

from .api.shared import api_resp
from .data.api.chats import ChatGroup
from .data.api.user import User as RawUser

if TYPE_CHECKING:
	from . import Bot



class Chat:
	def __init__(self, data: ChatGroup, bot: "Bot"):
		self.bot = bot


		self.id: str     = data._id
		self.created	 = data.created
		self.deleted	 = data.deleted
		self.last_active = data.last_active
		self.members	 = data.members
		self.owner	     = data.owner
		self.nickname  	 = data.nickname
		self.data        = data

	async def send_msg(self, message) -> Optional["Post"]:
		data, status = await self.bot.api.send_post(self.id, message)

		if status != 200:
			return None
		return await create_message(self.bot, data) # type: ignore


class Asset:
	def __init__(self, data: dict): # TODO: Type the raw format.
		self.filename = data["filename"]
		self.hight    = data["height"]
		self.id       = data["id"]
		self.mime     = data["mime"]
		self.size     = data["size"]
		self.width    = data["width"]

class User: 
	def __init__(self, data: RawUser):
		self.data: RawUser = data

		self.name         = self.data.name
		self.permissions  = self.data.permissions
		self.quote	  = self.data.quote
		self.id	          = self.data.uuid
		self.avatar_color = self.data.avatar_color

		if (self.data.avatar):
			self.pfp  = f"https://uploads.meower.org/icons/{self.data.avatar}"
		else:
			self.pfp  = f"https://raw.githubusercontent.com/3r1s_s/meo/main/images/avatars-webp/icon_{self.data.pfp_data}.webp"

class Post:
	def __init__(self, bot, user: User, _raw: dict, chat: Chat):
		self._bot = bot
		self._raw = _raw

		self.user: User    = user
		self.chat: Chat    = chat
		self.content: str  = self._raw["p"]
		self._id: str      = self._raw["post_id"]
		self.date          = datetime.fromtimestamp(self._raw["t"]["e"])
		self.attachments: list[Asset] = [Asset(data) for data in self._raw["assets"]]
		
	def __str__(self):
		return str(self.content)

	async def reply(self, message):
		return await self.chat.send_msg(
			f"@{self.user.name} \"{self.content[:20]}\" ({self._id})\n" + \
			f"{message}"
        )


class Context:
	def __init__(self, post: Post, bot):
		self.message = post
		self.user = self.message.user
		self._bot = bot

	async def send_msg(self, msg):
		return await self.message.chat.send_msg(msg)

	async def reply(self, msg):
		await self.message.reply(msg)

async def create_message(bot: "Bot", message: dict): 
	return Post(
          bot,
		  cast(User, await get_user(bot, message["u"])),
		  message,
		  cast(Chat, await bot.get_chat(message["post_origin"]))
	)

async def get_user(bot: "Bot", name: str) -> Optional[User]:
	if (user := bot.cache.get_user(name)): 
		return cast(User, user)
	
	data = (await bot.api.users.get(name))
	if (data[1] != 200): return

	user = User(cast(RawUser, data[0]))
	bot.cache.add_user(user)
	return user


