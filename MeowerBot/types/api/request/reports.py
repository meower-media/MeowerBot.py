from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, List, Literal


class UpdateReportBody:
    status: Literal["no_action_taken", "action_taken"]

class UpdateNotesBody:
    notes: str

class UpdateUserBanBody:
    state: Literal["none", "temp_restriction", "perm_restriction", "temp_ban", "perm_ban"]
    restrictions: int
    expires: int
    reason: str

class UpdateUserBody:
    permissions: Optional[int] = None

class UpdateChatBody:
    nickname: str

class InboxMessageBody:
    content: str

class NetblockBody:
    type: int

