from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json

from .reports import PagedRequest


@dataclass_json
@dataclass
class ChatGroup:
    _id: str
    created: int
    deleted: bool
    last_active: int
    members: List[str]
    nickname: Optional[str]
    owner: Optional[str]
    type: int


class Chats(PagedRequest[ChatGroup]): pass
