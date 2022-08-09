from typing import TYPE_CHECKING

from errors import *

if TYPE_CHECKING:
    from cloudlink import CloudLink

    from .. import Bot


class User:
    """A user in meower"""

    def __init__(self, username: str, cloudlink: CloudLink) -> None:
        self.name = username
        self._wss = cloudlink

    def mention(self, msg: str):
        """Mentions the user"""
        self._wss.sendPacket({"cmd": "post_home", "val": f"@{self.name} {msg}"})


class Message:
    """A meower Msg in Class form"""

    def __init__(self, text: str, user: User, cloudlink: CloudLink) -> None:
        self.txt: str = text
        self.sender: User = user
        self._wss = cloudlink

    def reply(self, msg):
        """
        Reply to the msg

        sends '[reply to {original_msg}] {msg}'
        """
        self.sender.mention(f"[reply to {self.text}] {msg}")
