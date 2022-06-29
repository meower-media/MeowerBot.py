
from sys import exit
from threading import ThreadError, Thread

from cloudlink import CloudLink
from meower import meower
from requests import get
from errors import *


class Client:

    def __init__(self, meower_username: str, meower_password: str, debug: bool = False) -> None:
        self._start_wait = 0
        self.authed = False
        self.callbacks = {}
        self.username = meower_username
        self.password = meower_password
        if meower.repairMode() or meower.argoTunnel():
            raise CantConnectError("Meower is down")

        self._wss = CloudLink(debug)

        self._wss.callback("on_packet", self._bot_packet_handle)
        self._lastpacket = {}

        self.default_callbacks()
        
        
    def _bot_packet_handle(self, packet: dict):
        if self.start:
            self.start = False
            import time
            
            self._wss.sendPacket({
                "cmd": 'direct',
                "val": {
                    "cmd": "ip", "val": get("https://api.meower.org/ip").text,
                }
            })
            time.sleep(1)
            self._wss.sendPacket({
                "cmd": 'direct',
                "val": {"cmd": 'type', "val": 'py'},
            })
            time.sleep(1)
            self._wss.sendPacket({
                "cmd": 'direct',
                "val": "meower",
            })
           
            self._wss.sendPacket({
                
                "cmd": "direct",
                "val": {"cmd": "authpswd", "val": {"username": self.username, "pswd": self.password}}
            })
            time.sleep(.1)
            self._login_callback(self._lastpacket["val"], packet)
        else:
            if False:
                pass
            
                
            else:
                self.callbacks["on_raw_msg"](packet["val"])
                
                    
        self._lastpacket = packet

    def _bot_api_loop(self):
        #not done yet
        #    self._wss.sendPacket({"cmd": "get_home"})
        pass
    def start(self):
        self.start = True
        self._wss.client("wss://server.meower.org")

        return self

    def _login_callback(self, send_return: dict, status_code: dict):
        assert send_return["mode"] == "auth"
        assert send_return["payload"]["username"] == self.username

        assert status_code["val"] == "I:100 | OK"

        self.authed = True

        self.BotLoopThread = Thread(target=self._bot_api_loop, args=(self))

        self.BotLoopThread.start()
        try:
            self.send_msg("")
        except BaseException as e:
            print(e)
    def send_msg(self, msg: str):
            self._wss.sendPacket({
                "cmd": "direct",
                "val": {
                    "cmd": "post_home", 
                    "val": msg
                }, 
                
            })
    def callback(self,func:callable):
        self.callbacks[func.__name__] = func
    def on_raw_msg(self,msg:dict):

            print(f"msg: {msg}")
            if not msg["u"] == self.username:
                self.send_msg("Testing")
        
    def default_callbacks(self):
        self.callback(self.on_raw_msg)
MeowerBot = Client("ShowierDataTest", "Gisd12102007",True)

MeowerBot.start()
