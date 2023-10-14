from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, List, Literal

@dataclass_json
@dataclass
class UpdateReportBody:
    status: Literal["no_action_taken", "action_taken"]

@dataclass_json
@dataclass
class UpdateNotesBody:
    notes: str

@dataclass_json
@dataclass
class UpdateUserBanBody:
    state: Literal["none", "temp_restriction", "perm_restriction", "temp_ban", "perm_ban"]
    restrictions: int
    expires: int
    reason: str

@dataclass_json
@dataclass
class UpdateUserBody:
    permissions: Optional[int] = None

@dataclass_json
@dataclass
class UpdateChatBody:
    nickname: str

@dataclass_json
@dataclass
class InboxMessageBody:
    content: str

@dataclass_json
@dataclass
class NetblockBody:
    type: int

