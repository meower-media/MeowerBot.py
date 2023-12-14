from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .reports import PagedRequest
from .user import User
from ..generic import Post


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
