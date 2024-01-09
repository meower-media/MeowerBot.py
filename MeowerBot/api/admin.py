from typing import Optional, Literal

from httpx import AsyncClient

from .shared import api_resp, post_resp
from ..data import generic
from ..data.api.reports import AdminNotesResponse, Report, ReportRequest


def notes_return(resp): return api_resp(AdminNotesResponse, resp)
def reports_return(resp): return api_resp(Report, resp)

# TODO: Implement wrapper for https://github.com/meower-media-co/Meower-Server/blob/better-moderation/rest_api/admin.py#L74-L1564


class Admin:
	def __init__(self, client: AsyncClient):
		self.client = client

	async def get_reports(self, timeout: Optional[int] = None):
		return api_resp(ReportRequest, await self.client.get("/admin/reports", timeout=timeout, params={"autoget": None}))

	async def get_report(self, uuid: generic.UUID):
		return reports_return(await self.client.get(f"/admin/reports/{uuid}/", params={"autoget": None}))

	async def edit_report(self, uuid: generic.UUID, status: Literal["no_action_taken", "action_taken"]):
		return reports_return(await self.client.patch(f"/admin/reports/{uuid}", json={"status": status}))

	async def escalate_report(self, uuid: generic.UUID):
		return reports_return(await self.client.post(f"/admin/reports/{uuid}/escalate/"))

	async def fetch_note(self, identifier: str):
		return notes_return(await self.client.get(f"/admin/notes/{identifier}", params={"autoget": None}))

	async def create_note(self, identifier: str, notes: str):
		return notes_return(await self.client.put(f"/admin/notes/{identifier}", json={"notes": notes}))

	async def get_post(self, uuid: generic.UUID):
		return post_resp(await self.client.get(f"/admin/posts/{uuid}", params={"autoget": None}))

	async def delete_post(self, uuid: generic.UUID):
		return post_resp(await self.client.delete(f"/admin/posts/{uuid}"))

	async def restore_deleted_post(self, uuid: generic.UUID):
		return post_resp(await self.client.post(f"/admin/posts/{uuid}/restore"))
