from httpx import AsyncClient, Auth
import ujson as json
from ..data import generic
from ..data.api.reports import ReportRequest, Report, AdminNotesResponse, PagedRequest
from ..data.generic import Post
from ..data.api.chats import Chats, ChatGroup
from ..data.api.user import User, Relationship

from typing import Literal
from httpx import Response

from .shared import api_resp
from urllib.parse import urljoin

class User:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def _get(self, username, url, json=None, page=1, query = None, params=None):
        return await self.client.get(urljoin(f"/users/{username}/", url), json=json, params={"q": query, "p": page, **params})

    async def get_posts(self, username, query, page = 1):
        return api_resp(PagedRequest[Post], await self._get(username, "posts", query=query, page=page, params={"autoget": None}))

    

    async def get_relationship(self, username):
        return api_resp(Relationship, await self._get(username, "relationship"))
    
    async def edit_relationship(self, username, state: Literal[0, 1, 2]):
        return api_resp(Relationship, await self.client.patch(f"/users/{username}/relationship", json={"state": state}))

    async def dm(self, username):
        return api_resp(ChatGroup, self._get(username, 'dm'))
