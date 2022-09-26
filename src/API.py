import asyncio
from urllib.parse import urljoin

import aiohttp


class MeowerAPI:
    MeowerURI = "https://api.meower.org"
    session = None

    def __init__(self, username):
        self.username = username
        self._token = None

    async def __aenter__(self):
        await self.init()

    async def __aexit__(self):
        await self.session.close()
        await asyncio.wait(0)

    async def init(self):
        headers = {"username": self.username, "token": self._token}
        self.session = await aiohttp.ClientSession(headers=headers)

    def add_token(self, token):
        self._token = token

    async def status(self) -> dict:
        async with self.session.get(urljoin(self.MeowerURI, "/status")) as resp:
            if resp.status != 200:  # assume Error
                return {"isRepairMode": True, "scratchDeprecated": False}
            return await resp.json()

    async def get_user(self, username) -> dict:
        async with self.session.get(
            urljoin(self.MeowerURI, f"/users/{username}")
        ) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

    async def get_posts_chat(self, chat, auto_get=False, page=None) -> list:
        args = "?"
        if auto_get:
            args += "autoget&"
        if page is not None:
            args += f"page={page}"
        async with self.session.get(
            urljoin(self.MeowerURI, f"/posts/{chat}{args}")
        ) as resp:
            if resp.status != 200:
                return None
            return await resp.json()
