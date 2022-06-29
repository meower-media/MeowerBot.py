from threading import ThreadError, Thread

from cloudlink import CloudLink
from meower import meower
from requests import get

from json import dumps,loads

from .errors import *

class Client:
    def ping(self): 
        self._wss.sendPacket({"cmd": "ping", "val": ""})
    def __init__(self, meower_username: str, meower_password: str, debug: bool = False) -> None:
        self.job_thread = Thread(None,self._bot_api_loop,args=())
        self._start_wait = 0
        self.authed = False
        self.callbacks = {}
        self.username = meower_username
        self.password = meower_password
        try:
            if meower.repairMode() or meower.argoTunnel():
                raise CantConnectError("Meower is down")
        except IndexError:
            if meower.repairMode():
                raise CantConnectError("Meower Is down")
        self._wss = CloudLink(debug)

        
        self._wss.callback("on_packet", self._bot_packet_handle)
        self._lastpacket = {}

        self.default_callbacks()
        
        
    def _bot_packet_handle(self, packet: dict):
        packet = loads(packet)
        if self.start_attr:
            self.start_attr = False
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
            time.sleep(.8)
            
            self._login_callback(packet)
        else:
            if packet["cmd"] == "statuscode":
                self.server_status = packet["val"]
            
            elif packet["cmd"] == "":
                raise NotImplementedError
               
            else:
                self.callbacks["on_raw_msg"](packet["val"])
        
                    
        self._lastpacket = packet

    def _bot_api_loop(self):
        import time
        while self.authed:
            time.sleep(60)
            self.ping()
        pass
    def start(self):
        self.start_attr = True
        self._wss.client("wss://Server.meower.org")

        if not self.authed:
            raise CantConnectError("Meower Is down")

    def _login_callback(self, status_code: dict):


        self.authed = True

        
        
        try:
            print("sending start msg")
            self.send_msg(f"{self.username} is online now")
        except BaseException as e:
            print(e)
        
        
        self.job_thread.start()
    def send_msg(self, msg: str):
            self._wss.sendPacket({
                "cmd": "direct",
                "val": {
                    "cmd": "post_home", 
                    "val": msg
                }})
    def callback(self,func:callable):
        self.callbacks[func.__name__] = func
    def on_raw_msg(self,msg:dict):

            print(f'msg: {msg["u"]}: {msg["p"]}')
            if not msg["u"] == self.username:
                if msg["u"] == "Discord":
                    msg["u"] = msg["p"].split(":")[0]
                    msg["p"] = msg["p"].split(":")[1].strip() 
                if msg["p"].startswith(f'@{self.username}'):   
                    self.send_msg(f'Hello, {msg["u"]}!')
        
    def default_callbacks(self):
        self.callback(self.on_raw_msg)

