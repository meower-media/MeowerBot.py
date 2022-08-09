import os
import sys
import time
from json import loads
from subprocess import run
from threading import Thread

from cloudlink import CloudLink
from requests import get
from websocket import WebSocketConnectionClosedException

from .errors import *


class Client:
    """
    The Websocket client/bot class

    attributes:

    - authed: bool

        if the client is authed

    - callbacks: dict[callable]

        packet callbacks

    - username: str

        User defined username

    - password: str

        user defined password

    methods:

    - ping

    - start


    - callback

    - send_msg

    - send_pvar

    - send_pmsg


    """

    def ping(self):
        """
        Pings the server

        you dont need to call this unless you overide _bot_api_loop
        """
        self._wss.sendPacket({"cmd": "ping", "val": ""})

    def __init__(
        self,
        meower_username: str,
        meower_password: str,
        debug: bool = False,
        auto_reconect: bool = True,
        reconect_time: float = 1,
    ) -> None:
        self.job_thread = Thread(None, self._bot_api_loop, args=(), daemon=True)
        self.job_thread.name = "MeowerBot_Loop"
        self._start_wait = 0
        self.authed = False
        self.callbacks = {}
        self.start_attr = True
        self.server_status = "I:0: Test"
        self.auto_reconect = auto_reconect
        self.auto_reconect_time = reconect_time
        self.username = meower_username
        self.password = meower_password
        self.currently_connecting = True

        self._wss = CloudLink(debug)
        self.ulist = self._wss.userlist

        self._wss.callback("on_packet", self._bot_packet_handle)
        self._wss.callback("on_error", self._bot_on_error)
        self._wss.callback("on_close", self._bot_on_close)
        self._wss.callback("on_connect", self._bot_on_connect)

        self._lastpacket = {}

        self.default_callbacks()

    def _call_callbacks(self, callback, args):
        if callback in self.callbacks:
            for callback in self.callbacks[callback]:
                callback(*args)

    def _bot_packet_handle(self, packet: dict):
        """
        Handles the packets for the bot
        """
        packet = loads(packet)

        if ("listener" in packet):

            listerner = {"detected": True, "listener": packet["listener"] }
        else:
            listerner = {"detected": False, "listener":"" }
        

        if packet["cmd"] == "statuscode":
            self._call_callbacks("on_status_change", (packet["val"], listerner))
        elif packet["cmd"] == "pvar":
            
                # possible err, forgot keys of
            self._call_callbacks("handle_pvar", (
                packet["val"], packet["origin"], packet["name"], listerner
            ))


        elif packet["cmd"] == "pmsg":
           
            self._call_callbacks("handle_pmsg",(packet["val"], packet["origin"], listerner))
        
        elif packet["cmd"] == "ulist":
            self.ulist = self._wss._get_ulist
        elif packet["cmd"] == "":
            raise NotImplementedError

        else:
            if "post_origin" in packet["val"]:
                self._call_callbacks("on_raw_msg",(packet["val"], listerner))
            else:
                self._call_callbacks("on_raw_packet", (packet, listerner))
            
        
    @property
    def get_ulist(self):
        """gets the u!ist from meower"""
        return self.ulist

    def _bot_on_connect(self):

        self._wss.sendPacket(
            {
                "cmd": "direct",
                "val": {
                    "cmd": "ip",
                    "val": get("https://api.meower.org/ip").text,
                },
            }
        )
        time.sleep(1)
        self._wss.sendPacket(
            {
                "cmd": "direct",
                "val": {"cmd": "type", "val": "py"},
            }
        )
        time.sleep(1)
        self._wss.sendPacket(
            {
                "cmd": "direct",
                "val": "meower",
            }
        )

        self._wss.sendPacket(
            {
                "cmd": "direct",
                "val": {
                    "cmd": "authpswd",
                    "val": {"username": self.username, "pswd": self.password},
                },
            }
        )
        time.sleep(0.8)

        self._login_callback()
        self.currently_connecting= False
        self._call_callbacks("on_login", ())

    def _bot_on_close(self):
        self._call_callbacks("on_close", (self.auto_reconect))

        if self.auto_reconect:
            if not self.currently_connecting:
                self.currently_connecting = True
                time.sleep(self.auto_reconect_time)
                self._wss.state = 0
                self.start()

    def _bot_on_error(self, e):
        if type(e) is KeyboardInterrupt:
            self._call_callbacks("on_close", (True))
            sys.exit()

        elif type(e) is WebSocketConnectionClosedException:
            self._bot_on_close()

        self._call_callbacks("on_error", (e))

    def _bot_api_loop(self):

        while self.authed:
            time.sleep(60)
            self.ping()
        pass

    def start(self):
        """
        Starts the wss, and runs the bot
        """
        self.start_attr = True
        self._wss.client("wss://server.meower.org/")

        if not self.authed:
            raise CantConnectError("Meower Is down")

    def _login_callback(self):
        if not self.authed:
            self.authed = True

        self.job_thread.start()

    def send_msg(self, msg: str):
        """
        sends a msg to the server

        takes:
            msg: Str
        """
        self._wss.sendPacket({"cmd": "direct", "val": {"cmd": "post_home", "val": msg}})

    def send_pmsg(self, val, user):
        """
        sends private msg to spesified user
        """
        self._wss.sendPacket({"cmd": "pmsg", "val": val, "id": user})

    def send_pvar(self, user, var_name, val):
        self._wss.sendPacket({"cmd": "pvar", "name": var_name, "val": val, "id": user})

    def callback(self, func: callable):

        """
        Makes a callback for commands and stuff like that

        takes:

        - func: callable
            gets callback name from it, and uses it as the callback
        """
        if func.__name__ in self.callbacks:
            self.callbacks[func.__name__].append(func)
        else:
            self.callbacks[func.__name__]= [func]
     
    def on_status_change(self, statuscode, wadtcher):
        self.statuscode = statuscode   
    
    def default_callbacks(self):
        """
        sets the callbacks back to there original callbacks
        """
        self.callbacks = {}
        self.callback(self.on_status_change)