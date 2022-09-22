from .cloudlink import Cloudlink
from .Errors import LoginError, PostError


class Bot:
    def __init__(self, username, password, logs=False):
        self.cl = CloudLink()
        self.wss = self.cl.client(logs=logs, async_client=True)

        self.username = username
        self._psw = password
        self.authed = False
        self.BotID = None

        self.callbacks = {}

        self.internal_cbs = _bot_callbacks(self)

    async def send_msg(self, msg, where="home"):
        if where == "home":
            await self.wss.sendCustom("post_home", msg, listener="MsgListener")
        else:
            await self.wss.sendCustom(
                "post_chat", {"p": msg, "chatid": where}, listener="MsgListener"
            )

    def callback(self, callback, callbackid=None):
        callbackid = callbackid or callback.__name__
        if callbackid in self.callbacks.keys():
            self.callbacks[callbackid].append(callback)
        else:
            self.callbacks[callbackid] = [callback]
        return self


class _bot_callbacks:
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

        print("on_close fired!")

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
            if msg["listener"] == "LoginDone":
                if code == self.cl.supporter.codes["OK"]:
                    self.bot.BotID = myClientObject
                    self.bot.authed = True

                    self._call_callbacks(
                        "on_login", kwargs={"id": self.wss.myClientObject}
                    )
                else:
                    raise LoginError(code)
            elif msg["Listener"] == "MsgListener":
                if not code == self.cl.supporter.codes["OK"]:
                    raise PostErorr(code)  # raises an error if a post could not be sent
        await self._call_callbacks(
            "on_statuscode",
            args=(code, message),
            kwargs={
                "listener": {
                    "detected": "listener" in message.keys(),
                    "id": value["listener"] if "listener" in value.keys() else None,
                }
            },
        )

    async def _bot_on_pvar(
        self, var_name: str, var_value: any, origin: any
    ):  # Called when a packet is received with the pvar command.
        await self._call_callbacks(
            "on_statuscode",
            args=(var_name, var_value, origin),
        )

    async def _bot_on_pmsg(
        self, value: str, origin: any
    ):  # Called when a packet is received with the pmsg command.
        await self._call_callbacks(
            "on_statuscode",
            args=(value, origin),
            kwargs={
                "listener": {
                    "detected": "listener" in value.keys(),
                    "id": value["listener"] if "listener" in value.keys() else None,
                }
            },
        )
