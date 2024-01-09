
from httpx import AsyncClient

from .admin import Admin
from .chats import Chats
from .shared import api_resp, post_resp
from .user import User as API_USER_WRAPPER
from ..data import generic
from ..data.api.reports import PagedRequest
from ..data.generic import Post


class MeowerAPI:
	base_uri = "https://api.meower.org/"

	admin: Admin
	chats: Chats
	users: API_USER_WRAPPER

	def __init__(self, username):
		self.headers = {"username": username, "user-agent": 'Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/118.0 Firefox/118.0'}
		self.client = AsyncClient(headers=self.headers, base_url=self.base_uri, follow_redirects=True)

		self.admin = Admin(self.client)
		self.chats = Chats(self.client)
		self.users = API_USER_WRAPPER(self.client)



	async def login(self, token):
		self.client.headers.update({"token": token})
		self.headers.update({"token": token})

	# basic bot functionalilty that needs to stay in MeowerAPI

	async def get_posts(self, chat: str | generic.UUID, page: int = 1):
		if chat == "home":
			resp = await self.client.get("/home/", params={"page": page, "autoget": None})
		else:
			resp = await self.client.get(f"/posts/{chat}", params={"page": page, "autoget": None})

		return api_resp(PagedRequest[Post], resp)

	async def send_post(self, chat: str | generic.UUID, content: str):
		if chat == "home":
			resp = await self.client.post("/home/", json={"content": content})
		else:
			resp = await self.client.post(f"/posts/{chat}", json={"content": content})

		return post_resp(resp)

	async def get_post(self, uuid: generic.UUID):
		return post_resp(await self.client.get("/posts", params={"id": uuid}))


	async def update_post(self, uuid: generic.UUID,  content: str) -> Post:
		return post_resp(await self.client.patch("/posts", params={"id": uuid}, json={"content": content}))

	async def delete_post(self, uuid: generic.UUID) -> Post:
		return post_resp(await self.client.patch("/posts", params={"id": uuid}))


	async def get_inbox(self):
		return api_resp(PagedRequest[Post], await self.client.get("/inbox", params={"autoget": None}))

	async def search_users(self, query: str, page: int = 1, ):
		return api_resp(PagedRequest[Post], await self.client.get("/search/users", params={"q": query, "p": page, "autoget": None}))

	async def search_home(self, query: str, page: int = 1):
		return api_resp(PagedRequest[Post], await self.client.get("/search/home", params={"q": query, "p": page, "autoget": None}))
