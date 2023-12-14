
from dataclasses import dataclass, field

from dataclasses_json import config, dataclass_json

from ..generic import BitFlag, UUID


class UserFlags:
    SYSTEM = 1
    DELETED = 2
    PROTECTED = 4


class Permissions:
    SYSADMIN = 1

    VIEW_REPORTS = 2
    EDIT_REPORTS = 4

    VIEW_NOTES = 8
    EDIT_NOTES = 16

    VIEW_POSTS = 32
    DELETE_POSTS = 64

    VIEW_ALTS = 128
    SEND_ALERTS = 256
    KICK_USERS = 512
    CLEAR_USER_QUOTES = 1024
    VIEW_BAN_STATES = 2048
    EDIT_BAN_STATES = 4096
    DELETE_USERS = 8192

    VIEW_IPS = 16384
    BLOCK_IPS = 32768

    VIEW_CHATS = 65536
    EDIT_CHATS = 131072

    SEND_ANNOUNCEMENTS = 262144


class Restrictions:
    HOME_POSTS = 1
    CHAT_POSTS = 2
    NEW_CHATS = 4
    EDITING_CHAT_NICKNAMES = 8
    EDITING_QUOTE = 16


@dataclass_json
@dataclass
class User:
    name: str = field(metadata=config(field_name="_id"))
    banned: bool
    created: int
    error: bool
    flags: BitFlag
    last_seen: int
    lower_username: str
    lvl: int
    permissions: BitFlag
    pfp_data: int
    quote: str
    uuid: UUID

@dataclass_json
@dataclass
class Relationship:
    username: str
    state: int
    updated_at: int