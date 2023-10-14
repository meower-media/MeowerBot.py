from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import List, TypeVar, Generic, Optional, NewType


from ..generic import Post, UUID
from .reports import PagedRequest
from .user import User

class Inbox(PagedRequest[Post]): pass
class PostList(PagedRequest[Post]): pass
class UserList(PagedRequest[User]): pass

@dataclass_json
@dataclass
class Statistics:
    chats: int
    error: bool
    posts: int
    users: int
