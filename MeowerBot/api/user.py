from typing import Literal
from urllib.parse import urljoin

from httpx import AsyncClient

from .shared import api_resp
from ..data.api.chats import ChatGroup
from ..data.api.reports import PagedRequest
from ..data.api.user import (
	Relationship
)
from ..data.generic import Post


class User:
	def __init__(self, client: AsyncClient) -> None:
		self.client = client

	async def _get(self, username, url, page=1, query=None, params=None):

		if query is None:
			query = dict()

		if params is None:
			params = dict()

		return await self.client.get(urljoin(f"/users/{username}/", url), params={"q": query, "p": page, **params})

	async def get_posts(self, username, query, page=1):
		return api_resp(PagedRequest[Post], await self._get(username, "posts", query=query, page=page, params={"autoget": None}))

	async def get_relationship(self, username):
		return api_resp(Relationship, await self._get(username, "relationship"))

	async def edit_relationship(self, username, state: Literal[0, 1, 2]):
		return api_resp(Relationship, await self.client.patch(f"/users/{username}/relationship", json={"state": state}))

	async def dm(self, username):
		return api_resp(ChatGroup, await self._get(username, 'dm'))
