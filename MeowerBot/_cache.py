import time
from typing import Dict, Tuple, Any

from MeowerBot.context import Chat, User
from MeowerBot.data.generic import UUID

# 5 hours
CASHE_EXPIRATION = 60 * 60 * 5


class Cache:
	chats: Dict[str, Tuple[float, Chat]]
	users: Dict[str, Tuple[float, User]]

	def __init__(self):
		self.bots  = {}
		self.chats = {}
		self.users = {}

	def get_user(self, user_id: str) -> User | None | bool:
		if user_id not in self.users:
			return None

		user = self.users[user_id]
		if user[0] + CASHE_EXPIRATION < time.time():
			self.users.pop(user_id)
			return None

		if not isinstance(user[1], User):
			self.users.pop(user_id)
			return False

		return user[1]

	def add_user(self, user: User):
		if not user:
			return

		if user.id in self.users: # Theoretically should never happen, but a user may end up running wo checking it before
			return

		self.users[user.id] = (time.time(), user)

	def get_chat(self, chat_id: UUID) -> Chat | None:
		if chat_id not in self.chats:
			return None

		chat = self.chats[chat_id]
		if chat[0] + CASHE_EXPIRATION < time.time():
			self.chats.pop(chat_id)
			return None

		return chat[1]

	def add_chat(self, chat: Chat):
		if not chat:
			return

		# again should never happen
		if chat.id in self.chats:
			return

		self.chats[chat.id] = (time.time(), chat)


