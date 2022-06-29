from typing import TYPE_CHECKING
from errors import *
from meower import meower

if TYPE_CHECKING:
    from cloudlink import CloudLink
    from .. import Bot 
    
class User:
    def __init__(self,username:str,cloudlink:CloudLink) -> None:
        self.name = username
        self._wss = cloudlink
    
    def mention(self,msg:str):
        self._wss.sendPacket({
            "cmd":"post_home",
            "val": f"@{self.name} {msg}"
        })
    
class Message:
    def __init__(self,text:str,user:User,cloudlink:CloudLink) -> None:
        self.txt:str = text
        self.sender:User = user
        self._wss = CloudLink
    
    def reply(self,msg):
        self.sender.mention(f"[reply to {self.text}] {msg}")
        
    