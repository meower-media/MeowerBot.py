
from urllib.parse import urljoin
from httpx import AsyncClient, Auth
import ujson as json
from .types import generic
from .types.api.reports import ReportRequest, Report, AdminNotesResponse
from .types.api.request.reports import UpdateReportBody, UpdateNotesBody
from .types.api.request.chats import ChatBody
from .types.generic import Post
from .types.api.chats import Chats, ChatGroup

class MeowerAPI:
    base_uri = "https://api.meower.org/"

    def __init__(self, username):
        self.headers = {"username": username}
        self.client = AsyncClient(headers=self.headers, base_url=self.base_uri, params={"autoget": None})



    async def login(self, token):
        self.headers.update({"token": token})
    
    async def admin_get_reports(self, timeout=None) -> ReportRequest:
        resp = await self.client.get("/admin/reports", timeout=timeout)

        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Not found") 

        return ReportRequest.from_json(
            
        )
    
    async def admin_get_report(self, uuid: generic.UUID) -> Report:
        resp = await self.client.get(f"/admin/reports/{uuid}/")
        
        if resp.status_code == 403:
            raise RuntimeError("[API] 403 Found: You are not allowed to look at reports")
        

        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Not found") 

        return Report.from_json(resp.text)
    
    async def admin_edit_report(self, uuid: generic.UUID, **kwargs: UpdateReportBody) -> Report:
        resp = await self.client.patch(f"/admin/reports/{uuid}", json=kwargs)
        
        if resp.status_code == 403:
            raise RuntimeError("[API] 403 Found: You are not allowed to edit reports")
        
        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Not found") 

        return Report.from_json(resp.text)
    
    async def admin_escalate_report(self, uuid: generic.UUID) -> Report:
        resp = await self.client.post(f"/admin/reports/{uuid}/escalate/")
        if resp.status_code == 403:
            raise RuntimeError("[API] 403 Found: You are not allowed to edit reports")
        
        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Not found") 

        return Report.from_json(resp.text)
    
    async def admin_fetch_note(self, indentifier: str) -> AdminNotesResponse:
        resp = await self.client.get(f"/admin/notes/{indentifier}")
        
        if resp.status_code == 403:
            raise RuntimeError("[API] 403 Found: You are not allowed to look at notes")
        
        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Not found") 

        return AdminNotesResponse.from_json(resp.text)
    
    async def admin_create_note(self, indentifier: str, **kwargs: UpdateNotesBody) -> AdminNotesResponse:
        resp = await self.client.put(f"/admin/notes/{indentifier}", json=kwargs)
        if resp.status_code == 403:
            raise RuntimeError("[API] 403 Found: You are not allowed to edit/create notes")
        
        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Not found") 

        return AdminNotesResponse.from_json(resp.text)

    async def admin_get_post(self, uuid: generic.UUID) -> Post:
        resp = await self.client.get(f"/admin/posts/{uuid}")
        if resp.status_code == 403:
            raise RuntimeError("[API] 403 Found: You are not allowed to look at posts")
        
    
        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Not found") 

        return Post.from_json(resp.text)
    
    async def admin_delete_post(self, uuid: generic.UUID) -> Post:
        resp = await self.client.delete(f"/admin/posts/{uuid}")
        if resp.status_code == 403:
            raise RuntimeError("[API] 403 Found: You are not allowed to delete posts")
        

        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Not found") 

        return Post.from_json(resp.text)

    async def admin_restore_deleted_post(self, uuid: generic.UUID) -> Post:
        resp = await self.client.post(f"/admin/posts/{uuid}/restore")
        if resp.status_code == 403:
            raise RuntimeError("[API] 403 Found: You are not allowed to restore posts")
        
        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Not found") 

        return Post.from_json(resp.text)

    
    
    async def get_chats(self) -> Chats:
        resp = await self.client.get(f"/chats/")

        if resp.status_code == 401:
            raise RuntimeError("[API] No Token or username supplied! This is required to send authenticated API requests")

        return Chats.from_json(resp.text)
    
    async def create_chat(self, **kwargs: ChatBody) -> ChatGroup:
        resp = await self.client.post(f"/chats/", json=kwargs)

        if resp.status_code == 401:
            raise RuntimeError(json.parse(resp.text)["type"])
        
        return ChatGroup.from_json(resp.text)

    async def get_chat(self, uuid: generic.UUID) -> ChatGroup:
        resp = await self.client.get(f"/chats/{uuid}")

        if resp.status_code == 401:
            raise RuntimeError("[API] No Token or username supplied! This is required to send authenticated API requests")


        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Chat Not found") 

        return ChatGroup.from_json(resp.text)
    
    async def update_chat(self, uuid: generic.UUID, **kwargs: ChatBody) -> ChatGroup:
        resp = await self.client.patch(f"/chats/{uuid}", josn=kwargs)

        if resp.status_code == 429:
            raise RuntimeError("[API] Ratelimited: Updating chat")


        if resp.status_code == 401:
            raise RuntimeError("[API] No Auth to do this action")


        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Chat Not found") 
        

        return ChatGroup.from_json(resp.text)
    
    async def leave_chat(self, uuid: generic.UUID) -> dict:
        resp = await self.client.delete(f"/chats/{uuid}")


        if resp.status_code == 429:
            raise RuntimeError("[API] Ratelimited: Updating chat")


        if resp.status_code == 401:
            raise RuntimeError("[API] No Auth to do this action")


        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Chat Not found") 
        
        return {"error": False}

    async def add_user_to_chat(self, uuid: generic.UUID, username: str) -> ChatGroup:
        resp = await self.client.put(f"/chats/{uuid}/members/{username}")

        if resp.status_code == 429:
            raise RuntimeError("[API] Ratelimited: Updating chat")


        if resp.status_code == 401:
            raise RuntimeError("[API] No Auth to do this action")


        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Chat Not found") 

        return ChatGroup.from_json(resp.text)
    
    async def transfer_chat_ownership(self, uuid: generic.UUID, username: str) -> ChatGroup:
        resp = await self.client.post(f"/chats/{uuid}/members/{username}/transfer")

        if resp.status_code == 429:
            raise RuntimeError("[API] Ratelimited: Updating chat")


        if resp.status_code == 401:
            raise RuntimeError("[API] No Auth to do this action")


        if resp.status_code == 404: 
            raise RuntimeError("[API] 404 Chat Not found") 

        return ChatGroup.from_json(resp.text)

    # TODO: Implement wrapper for https://github.com/meower-media-co/Meower-Server/blob/better-moderation/rest_api/admin.py#L74-L1564
    # TODO: https://github.com/meower-media-co/Meower-Server/blob/better-moderation/rest_api/home.py
    # TODO: https://github.com/meower-media-co/Meower-Server/blob/better-moderation/rest_api/posts.py
    # TODO: https://github.com/meower-media-co/Meower-Server/blob/better-moderation/rest_api/inbox.py
    # TODO: https://github.com/meower-media-co/Meower-Server/blob/better-moderation/rest_api/search.py
    # TODO: https://github.com/meower-media-co/Meower-Server/blob/better-moderation/rest_api/users.py
