import asyncio

from .Errors import LoginError, PostError


class _bot_callbacks:
    """Internal class for clarity"""

    def __init__(self, bot):
        self.bot = bot
        self.wss = self.bot.wss

    # skipcq
    async def on_connect(self):  # Called when the client is connected to the server.
        await self.wss.sendCustom(
            "authpswd",
            {"username": self.bot.username, "pswd": self.bot._psw},  # skipcq
            listener="loginDone",
        )

    # skipcq
    async def _call_callbacks(self, callback_id, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        if not callback_id in self.callbacks.keys():
            return

        not_awaited = []

        for cb in self.bot.callbacks:
            not_awaited.append(cb(*args, **kwargs, bot=self.bot))

        # skipcq
        _tmp_ = await asyncio.gather(*not_awaited)  # ignore all returns

    # skipcq
    async def _bot_on_close(
        self, close_status_code, close_msg
    ):  # Called when the client is disconnected from the server.

        await self._call_callbacks("on_close", args=(close_status_code, close_msg))

    # skipcq
    async def _bot_on_error(
        self, error
    ):  # Called when the client encounters an exception.
        # passed right through
        await self._call_callbacks("on_error", args=(error))

    # Below are templates for binding command-specific callbacks.
    # skipcq
    async def _bot_on_direct(
        self, message: any, origin: any, listener_detected: bool, listener_id: str
    ):
        if "post_origin" in message["val"]:
            await self._call_callbacks("on_raw_msg", args=(message))

        elif "mode" in message["val"] and message["val"]["mode"] == "auth":
            self.bot.api.add_token(message["val"]["payload"]["token"])
            await self.bot.api.init()

        else:
            await self._call_callbacks(
                "on_direct",
                args=(message, origin),
                kwargs={"listener": {"detected": listener_detected, "id": listener_id}},
            )

    # skipcq
    async def _bot_on_ulist(
        self, ulist: list
    ):  # Called when a packet is received with the ulist command.
        self._call_callbacks("on_ulist_change", args=(ulist))

    # skipcq
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

    # skipcq
    async def _bot_on_pvar(
        self, var_name: str, var_value: any, origin: any
    ):  # Called when a packet is received with the pvar command.
        await self._call_callbacks(
            "on_pvar",
            args=(var_name, var_value, origin),
        )

    # skipcq
    async def _bot_on_pmsg(
        self, value: str, origin: any
    ):  # Called when a packet is received with the pmsg command.
        await self._call_callbacks("on_pmsg", args=(value, origin))
