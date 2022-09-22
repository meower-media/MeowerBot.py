from .cloudlink import Cloudlink
from .Errors import LoginError, PostError


class Bot:
    def __init__(self, username, password, logs=False):
        self.cl = Cloudlink()
        self.wss = self.cl.client(logs=logs, async_client=True)

        self.username = username
        self._psw = password
        self.authed = False
        self.BotID = None

        self.callbacks = {}

        self.internal_cbs = _bot_callbacks(self)

        self.wss.callback(client.on_connect, self.internal_cbs._bot_on_connect)
        self.wss.callback(client.on_close, self.internal_cbs._bot_on_close)
        self.wss.callback(client.on_error, self.internal_cbs._bot_on_error)

        # Bind template callbacks
        self.wss.callback(client.on_direct, self.internal_cbs._bot_on_direct)
        self.wss.callback(client.on_ulist, self.internal_cbs._bot_on_ulist)
        self.wss.callback(client.on_statuscode, self.internal_cbs._bot_on_statuscode)
        self.wss.callback(client.on_pvar, self.internal_cbs._bot_on_pvar)
        self.wss.callback(client.on_pmsg, self.internal_cbs._bot_on_pmsg)

    async def send_msg(self, msg, where="home"):
      """
      Sends a msg to where the argument 'where' specified in meower
      """
        if where == "home":
            await self.wss.sendCustom("post_home", msg, listener="MsgListener")
        else:
            await self.wss.sendCustom(
                "post_chat", {"p": msg, "chatid": where}, listener="MsgListener"
            )

    def callback(self, callback, callbackid=None):
        """
        adds a callback to the bot
        """
        callbackid = callbackid or callback.__name__
        if callbackid in self.callbacks.keys():
            self.callbacks[callbackid].append(callback)
        else:
            self.callbacks[callbackid] = [callback]
        return self


class _bot_callbacks:
    """Internal class for clarity"""
    def __init__(self, bot):
        self.bot = bot
        self.wss = self.bot.wss

    async def on_connect(self):  # Called when the client is connected to the server.
        await self.wss.sendCustom(
            "authpswd",
            {"username": self.bot.username, "pswd": self.bot._psw},  # OK
            listener="loginDone",
        )

    async def _call_callbacks(self, callback_id, args=(), kwargs={}):
        if not callback_id in self.callbacks.keys():
            return

        for cb in self.bot.callbacks:
            await cb(*args, **kwargs, bot=self.bot)

    async def _bot_on_close(
        self, close_status_code, close_msg
    ):  # Called when the client is disconnected from the server.

        self._call_callbacks("on_close", args=(close_status_code))

    async def _bot_on_error(
        self, error
    ):  # Called when the client encounters an exception.
        # passed right through
        self._call_callbacks("on_error", args=(error))

    # Below are templates for binding command-specific callbacks.

    async def _bot_on_direct(
        self, message: any, origin: any, listener_detected: bool, listener_id: str
    ):
        if "post_origin" in message.keys():
            await self._call_callbacks("on_raw_msg", args=(message))
        else:
            self._call_callbacks(
                "on_direct",
                args=(message, origin),
                kwargs={
                    "listener": {"detected": listener_detected, "id": "listener_id"}
                },
            )

    async def _bot_on_ulist(
        self, ulist: list
    ):  # Called when a packet is received with the ulist command.
        self._call_callbacks("on_ulist_change", args=(ulist))

    async def _bot_handle_statuscode(
        self, code: str, message: any
    ):  # Called when a packet is received with the statuscode command.
        if "listener" in message.keys():
            if message["listener"] == "LoginDone":
                if code == self.cl.supporter.codes["OK"]:
                    self.bot.BotID = self.wss.myClientObject
                    self.bot.authed = True

                    self._call_callbacks(
                        "on_login", kwargs={"id": self.wss.myClientObject}
                    )
                else:
                    raise LoginError(code)
            elif message["Listener"] == "MsgListener":
                if not code == self.cl.supporter.codes["OK"]:
                    raise PostError(code)  # raises an error if a post could not be sent
        await self._call_callbacks(
            "on_statuscode",
            args=(code, message),
            kwargs={
                "listener": {
                    "detected": "listener" in message.keys(),
                    "id": message["listener"] if "listener" in message.keys() else None,
                }
            },
        )

    async def _bot_on_pvar(
        self, var_name: str, var_value: any, origin: any
    ):  # Called when a packet is received with the pvar command.
        await self._call_callbacks(
            "on_pvar",
            args=(var_name, var_value, origin),
        )

    async def _bot_on_pmsg(
        self, value: str, origin: any
    ):  # Called when a packet is received with the pmsg command.
        await self._call_callbacks(
            "on_pmsg",
            args=(value, origin)
        )
