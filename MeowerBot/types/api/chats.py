from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import List, TypeVar, Generic, Optional, NewType


from ..generic import Post, UUID
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
