import time
from typing import Dict, List, Tuple

from MeowerBot.context import Chat, PartialChat, PartialUser, User
from MeowerBot.data.generic import UUID

# 5 hours
CASHE_EXPIRATION = 60 * 60 * 5


class Cache:
	chats: Dict[UUID, Tuple[float, Chat | PartialChat]]
	users: Dict[str, Tuple[float, User | PartialUser]]
	bots:  Dict[str, float]

	def __init__(self):
		self.bots  = {}
		self.chats = {}
		self.users = {}

	def get_user(self, user_id: str) -> User | PartialUser | None:
		if user_id not in self.users:
			return None

		user = self.users[user_id]
		if user[0] + CASHE_EXPIRATION < time.time():
			self.users.pop(user_id)
			return None

		return user[1]

	def add_user(self, user: User):
		if not user:
			return

		if user.id in self.users: # Theoretically should never happen, but a user may end up running wo checking it before
			return

		self.users[user.id] = (time.time(), user)

	def get_chat(self, chat_id: UUID) -> Chat | PartialChat | None:
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

	def try_clear_bots(self):
		ret = []
		rem = []
		for username, timeout in self.bots.items():
			if timeout + CASHE_EXPIRATION < time.time():
				rem.append(username)
				continue

			ret.append(username)

		for user in rem:
			del self.bots[user]

		return ret

	def add_bot(self, user):
		if user in self.bots:
			self.bots[user] = time.time()
			return

		self.bots[user] = time.time()
		if user not in self.users:
			return

		self.users[user][1].is_bot = True

	def remove_bot(self, user):
		if user not in self.bots:
			return

		del self.bots[user]
		if user not in self.users:
			return

		self.users[user][1].is_bot = False
