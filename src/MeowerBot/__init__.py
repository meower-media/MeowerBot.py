import sys
import os
from subprocess import run
import time
from json import loads
from threading import Thread

from cloudlink import CloudLink
from meower import meower
from requests import get
from websocket import WebSocketConnectionClosedException
from .errors import *


class Client:
    """
    The Websocket client/bot class

    atrbutes:

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
        self._start_wait = 0
        self.authed = False
        self.callbacks = {}
        self.start_attr = True
        self.server_status = "I:0: Test"
        self.auto_reconect = auto_reconect
        self.auto_reconect_time = reconect_time
        self.username = meower_username
        self.password = meower_password
        self.ulist = "none"
        try:
            if meower.argoTunnel():
                raise CantConnectError("Meower is down")
        except IndexError:
            if meower.repairMode():
                raise CantConnectError("In Repair Mode")
        self._wss = CloudLink(debug)

        self._wss.callback("on_packet", self._bot_packet_handle)
        self._wss.callback("on_error", self._bot_on_error)
        self._wss.callback("on_close", self._bot_on_close)
        self._wss.callback("on_connect", self._bot_on_connect)

        self._lastpacket = {}

        self.default_callbacks()

    def _bot_packet_handle(self, packet: dict):
        """
        Handles the packets for the bot
        """
        packet = loads(packet)

        if packet["cmd"] == "statuscode":
            self.server_status = packet["val"]
        elif packet["cmd"] == "pvar":
            try:
                self.callbacks["handle_pvar"](packet["val"])
            except KeyError:
                pass

        elif packet["cmd"] == "pmsg":
            try:
                self.callbacks["handle_pmsg"](packet["val"])
            except KeyError:
                pass
        elif packet["cmd"] == "ulist":
            self.ulist = packet["val"].split(':')
        elif packet["cmd"] == "":
            raise NotImplementedError

        else:
            self.callbacks["on_raw_msg"](packet["val"])

        self._lastpacket = packet
        
    def get_ulist(self):
        """  gets the u!ist from meower"""


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

        try:
            self.callbacks["on_login"]()
        except KeyError:
            pass

    def _bot_on_close(self):
        try:
            self.callbacks["on_close"](
                self.auto_reconect
            )  # if the bot is actualy going to exit
        except KeyError:
            pass

        if self.auto_reconect:
            time.sleep(self.auto_reconect_time)
            self._wss.state = 0
            self.start()

    def _bot_on_error(self, e):
        if type(e) is KeyboardInterrupt:
            try:
                self.callbacks["on_close"](True)
            except KeyError:
                pass
            sys.exit()

        elif type(e) is WebSocketConnectionClosedException:
            self._bot_on_close() 
        
        try:
            self.callbacks["on_error"](e)
        except KeyError:
            print("ignoring error (no idea where)")
            if self._wss.debug:
                print(f"{type(e)}: {e}")

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
        self._wss.client("wss://Server.meower.org")

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
        self.callbacks[func.__name__] = func

    def on_raw_msg(self, msg: dict):
        """
        Base Raw Msg handler

        takes a msg, prints itm then says "Hello, {User}!"
        """
        print(f'msg: {msg["u"]}: {msg["p"]}')
        if not msg["u"] == self.username:
            if msg["u"] == "Discord":
                msg["u"] = msg["p"].split(":")[0]
                msg["p"] = msg["p"].split(":")[1].strip()
            if msg["p"].startswith(f"@{self.username}"):
                self.send_msg(f'Hello, {msg["u"]}!')

    def default_callbacks(self):
        """
        sets the callbacks back to there original callbacks
        """
        self.callbacks = {}
        self.callback(self.on_raw_msg)
