
import cloudlink
import sys

import json
import traceback

import requests


import time

class Bot:
    """
    A class that holds all of the networking for a meower bot to function and run

    """

    BOT_TAKEN_LISTENERS = [
        "__meowerbot__send_ip",
        "__meowerbot__send_message",
        "__meowerbot__login",
        "__meowerbot__cloudlink_trust",
    ]

    def __init__(self, debug=False, debug_out=sys.__stdout__):
        self.wss = cloudlink.CloudLink(debug=debug)
        self._stdout = sys.__stdout__
        self.debug = debug
        self.debug_out = debug_out

        self.callbacks = {}

        self.wss.callback(
            "on_packet", self._debug_fix
        )  # self._debug_fix catches all errors
        self.wss.callback("on_error", self.__handle_error__)  # handle uncought errors
        self.wss.callback("on_close", self.__handle_close__)  # Websocket disconnected
        self.wss.callback(
            "on_connect", self.__handle_on_connect__
        )  # signing in and stuff like that

        # to be used in start
        self.username = None
        self.password = None

    def run_cb(self, cbid, args=(), kwargs=None):  # cq: ignore
        if cbid not in self.callbacks:
            return  # ignore

        if not kwargs:
            kwargs = {}

        kwargs["bot"] = self
        print(kwargs, "\n", args)
        for callback in self.callbacks[cbid]:
            try:
                callback(
                	*args, **kwargs
                )  # multi callback per id is supported (unlike cloudlink 0.1.7.3 LOL)
            except Exception as e: #cq ignore
               if self.debug:
                  print(traceback.format_exc(), file=self.debug_out)
               self.run_cb("error", args=(e))

    def __handle_error__(self, e):
        self.run_cb("error", args=(e))

    def _debug_fix(self, packet):
        packet = json.loads(packet)  # Server bug workaround

        try:
            self.__handle_packet__(packet)
        except Exception as e:  # cq: skip #IDC ABOUT GENERAL EXCP
            if self.debug:
                print(traceback.format_exc() ,file=self.debug_out)
            self.run_cb("error", args=(e))

        try:
            self.run_cb("__raw__", args=(packet))  # raw packets
        except Exception as e:  # cq: skip #IDC ABOUT GENERAL EXCP
            if self.debug:
                print(traceback.format_exc(), file=self.debug_out)
            self.run_cb("error", args=(e))

    def __handle_on_connect__(self):
        self.wss.sendPacket(
            {
                "cmd": "direct",
                "val": {
                    "cmd": "ip",
                    "val": requests.get("https://api.meower.org/ip").text,
                },
                "listener": "__meowerbot__send_ip",
            }
        )

        self.wss.sendPacket(
                {
                    "cmd": "direct",
                    "val": {"cmd": "type", "val": "py"},
                }
            )

        self.wss.sendPacket(
                {
                    "cmd": "direct",
                    "val": "meower",
                    "listener": "__meowerbot__cloudlink_trust",
                }
            )


    def _handle_status(self, status, listener):
        if listener == "__meowerbot__cloudlink_trust":
            if not status == "I:100 | OK":
                raise RuntimeError("CloudLink Trust Failed")

            self.wss.sendPacket(
                {
                    "cmd": "direct",
                    "val": {
                        "cmd": "authpswd",
                        "val":{"username":self.username, "pswd":self._password}
                    },
                    "listener": "__meowerbot__login",
                }
            )

        elif listener == "__meowerbot__login":
            if not status == "I:100 | OK":
                raise RuntimeError("Password Or Username Is Incorrect")


            time.sleep(0.5)
            self.run_cb("login", args=(), kwargs={})

        elif listener == "__meowerbot__send_message":
            if status == "I:100 | OK":
                return  # This is just checking if a post went OK

            raise RuntimeError("Post Failed to send")

    def callback(self, callback, cbid=None):
        """Connects a callback ID to a callback"""
        if cbid is None: cbid = callback.__name__

        if cbid not in self.callbacks:
            self.callbacks[cbid] = []
        self.callbacks[cbid].append(callback)

    def __handle_close__(self, *args, **kwargs):
        self.run_cb("close", args=args, kwargs=kwargs)

    def __handle_packet__(self, packet):
        if packet["cmd"] == "statuscode":
            if (
                packet.get("listener", None) in self.BOT_TAKEN_LISTENERS
            ):  # Requried listeners for the bot
                self._handle_status(packet["val"], packet["listener"])
                print(packet)
                return
            else:
                listener = packet.get("listener", None)
                return self.run_cb("statuscode", args=(packet["val"], listener))

        elif packet["cmd"] == "ulist":
            self.run_cb("ulist", self.wss.statedata["ulist"]["usernames"])

        elif (
            packet["cmd"] == "direct" and "post_origin" in packet["val"]
        ):  # Message Handler
            # TODO: MAKE A CTX/MESSAGE OBJ SYSTEM.
            # POSSIBLY MAKE A BUILTIN CMD SYSTEM

            self.run_cb("message", args=(json.loads(packet["val"]),))
        elif packet["cmd"] == "direct":
            listener = packet.get("listener")
            self.run_cb("direct", args=(packet["val"], listener))

        else:
            listener = packet.get("listener")
            self.run_cb(packet["cmd"], args=(packet["val"], listener))

    def send_msg(self, msg, to="home"):
        if to == "home":
            self.wss.sendPacket(
                {"cmd": "direct", "val": {"cmd": "post_home", "val": msg}, "listener":"__meowerbot__send_message"}
            )
        else:
            self.wss.sendPacket(
                {
                    "cmd": "direct",
                    "val": {"cmd": "post_chat", "val": {"chatid": to, "p": msg}},
                    "listener":"__meowerbot__send_message"
                }
            )

    def run(self, username, password, server="wss://server.meower.org"):
        """
        Runs The bot (Blocking)
        """
        self.username = username
        self._password = password
        with self.debug_out as sys.stdout:
            self.wss.client(server)
