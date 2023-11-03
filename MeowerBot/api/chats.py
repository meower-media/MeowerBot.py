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

def chat_return(resp: Response):
    return api_resp(ChatGroup, resp)

class Chats:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client
    
    async def fetch_all(self) -> Chats:
        return api_resp(Chats, await self.client.get(f"/chats/", params={"autoget": None}))

    async def create(self, nickname: str) -> ChatGroup:
        return chat_return(await self.client.post(f"/chats/", json={"nickname": nickname}))

    async def get(self, uuid: generic.UUID) -> ChatGroup:
        return chat_return(await self.client.get(f"/chats/{uuid}", params={"autoget": None}))

    async def update(self, uuid: generic.UUID, nickname: str) -> ChatGroup:
        return chat_return(await self.client.patch(f"/chats/{uuid}", josn={"nickname": nickname}))

    async def leave(self, uuid: generic.UUID) -> dict:
        return api_resp(dict, await self.client.delete(f"/chats/{uuid}"))
    
    async def add_user(self, uuid: generic.UUID, username: str) -> ChatGroup:
        return chat_return(await self.client.put(f"/chats/{uuid}/members/{username}"))
    
    async def transfer_ownership(self, uuid: generic.UUID, username: str) -> ChatGroup:
        return chat_return(await self.client.post(f"/chats/{uuid}/members/{username}/transfer"))


