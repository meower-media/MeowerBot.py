# type: ignore

#!/usr/bin/env python3



version = "0.1.7.4"

# Server based on https://github.com/Pithikos/python-websocket-server
# Client based on https://github.com/websocket-client/websocket-client

"""
CloudLink by MikeDEV, ShowierData9978
Please see https://github.com/MikeDev101/cloudlink for more details.
0BSD License
Copyright (C) 2020-2022 MikeDEV Software, Co.
Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.
THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Modified for use in MeowerBot.py by ShowierData9978

- stripped everything server related
- made lib use logging insted of print
"""

import json
import threading
import websocket as ws_client  # type: ignore
import logging
import logging as log

"""
Code formatting
(Type):(Code) | (Description)
Type: Letter
    I - Info
    E - Error
Code: Number, defines the code
Description: String, Describes the code
"""


class API:
    def __init__(self, logging=None):
        self.logging = logging or log.getLogger("CloudLink")
        self.logging.debug("CloudLink API initialized")

        self.callback_function = {
            "error": self._on_error_client,  # type: ignore
            "connection": self._on_connection_client,  # type: ignore
            "closed_connection": self._closed_connection_client,  # type: ignore
            "packet": self._on_packet_client,  # type: ignore
        }

        self.statedata = {}

    def client(self, ip="ws://127.0.0.1:3000/"):  # Runs CloudLink in client mode.
        try:

            # Change the link state to 2 (Client mode)
            self.wss = ws_client.WebSocketApp(
                ip,
                on_message=self._on_packet_client,  # type: ignore
                on_error=self._on_error_client,  # type: ignore
                on_open=self._on_connection_client,  # type: ignore
                on_close=self._closed_connection_client,  # type: ignore
            )

            # Format dict for storing this mode's specific data
            self.statedata = {
                "ulist": {"usernames": []},
            }

            # Run the client
            self.wss.run_forever()
        except Exception as e:
            self.logging.error(f"Error at client: {e}")

    def stop(self, abrupt=False):  # Stops CloudLink (not sure if working)
        self.wss.close()

    def callback(
        self, callback_id, function
    ):  # Add user-friendly callbacks for CloudLink to be useful as a module
        try:
            if callback_id in self.callback_function:
                self.callback_function[callback_id] = function

                self.logging.debug(f"Binded callback {callback_id}.")
            else:
                self.logging.error(
                    f"Error: Callback {callback_id} is not a valid callback id!"
                )
        except Exception as e:
            self.logging.error(f"Error at callback: {e}")

    def sendPacket(
        self, msg
    ):  # User-friendly message sender for both server and client.
        try:

            self.logging.debug(f"Sending {json.dumps(msg)}")
            self.wss.send(json.dumps(msg))
        except Exception as e:
            self.logging.error(f"Error on sendPacket (client): {e}")

    def getUsernames(self):  # Returns the username list.
        return self.statedata["ulist"]["usernames"]


class CloudLink(API):
    def __init__(self):  # Initializes CloudLink
        self.wss = None  # Websocket Object
        self.userlist = []  # Stores usernames set on link
        self.callback_function = {  # For linking external code, use with functions
            "on_connect": None,  # Handles new connections (server) or when connected to a server (client)
            "on_error": None,  # Error reporter
            "on_packet": None,  # Packet handler
            "on_close": None,  # Runs code when disconnected (client) or server stops (server)
        }

        self.statedata = {}  # Place to store other garbage for modes
        self.logging = logging.getLogger("Cloudlink")

        self.logging.info(f"CloudLink v{str(version)}")  # Report version number

    @staticmethod
    def _is_json(data):  # Checks if something is JSON
        if type(data) is dict:
            return True
        try:
            tmp = json.loads(data)
            return True
        except Exception as e:
            return False

    def _on_connection_client(self, ws):  # Client-side connection handler
        try:

            self.logging.info("Connected")
            self.wss.send(
                json.dumps({"cmd": "direct", "val": {"cmd": "type", "val": "py"}})
            )  # Specify to the server that the client is based on Python
            if not self.callback_function["on_connect"] is None:

                def run(*args):
                    try:
                        self.callback_function["on_connect"]()
                    except Exception as e:
                        self.logging.error(f"Error on _on_connection_client: {e}")

                threading.Thread(target=run).start()
        except Exception as e:
            self.logging.info(f"Error on _on_connection_client: {e}")

    def _on_packet_client(self, ws, message):  # Client-side packet handler
        try:

            self.logging.debug(f"New packet: {message}")

            tmp = json.loads(message)
            if (("cmd" in tmp) and (tmp["cmd"] == "ulist")) and ("val" in tmp):
                self.statedata["ulist"]["usernames"] = str(tmp["val"]).split(";")
                del self.statedata["ulist"]["usernames"][
                    len(self.statedata["ulist"]["usernames"]) - 1
                ]

                self.logging.info(
                    f"Username list: {str(self.statedata['ulist']['usernames'])}"
                )

            if not self.callback_function["on_packet"] == None:

                def run(*args):
                    try:
                        self.callback_function["on_packet"](message)
                    except Exception as e:

                        self.logging.error(f"Error on _on_packet_client: {e}")

                threading.Thread(target=run).start()
        except Exception as e:
            self.logging.error(f"Error on _on_packet_client: {e}")

    def _on_error_client(self, ws, error):  # Client-side error handler
        try:

            self.logging.error(f"Error: {error}")
            if not self.callback_function["on_error"] is None:

                def run(*args):
                    try:
                        self.callback_function["on_error"](error)
                    except Exception as e:
                        self.logging.error(f"Error on _on_error_client: {e}")

                threading.Thread(target=run).start()
        except Exception as e:

            self.logging.error(f"Error on _on_error_client: {e}")

    def _closed_connection_client(
        self, ws, close_status_code, close_msg
    ):  # Client-side closed connection handler
        try:

            self.logging.info(
                f"Closed, status: {close_status_code} with code {close_msg}"
            )
            if not self.callback_function["on_close"] is None:

                def run(*args):
                    try:
                        self.callback_function["on_close"]()
                    except Exception as e:

                        self.logging.error(f"Error on _closed_connection_client: {e}")

                threading.Thread(target=run).start()
        except Exception as e:
            self.logging.error(f"Error on _closed_connection_client: {e}")
