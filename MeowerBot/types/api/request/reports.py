from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, List, Literal
from typing import TypedDict


class UpdateReportBody(TypedDict):
    status: Literal["no_action_taken", "action_taken"]

class UpdateNotesBody(TypedDict):
    notes: str

class UpdateUserBanBody(TypedDict):
    state: Literal["none", "temp_restriction", "perm_restriction", "temp_ban", "perm_ban"]
    restrictions: int
    expires: int
    reason: str

class UpdateUserBody(TypedDict):
    permissions: Optional[int] = None

class UpdateChatBody(TypedDict):
    nickname: str

class InboxMessageBody(TypedDict):
    content: str

class NetblockBody(TypedDict):
    type: int

