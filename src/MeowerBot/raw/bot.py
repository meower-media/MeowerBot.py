from ._internal import _bot_callbacks
from .API import MeowerAPI
from .cloudlink import Cloudlink


class Bot:
    """
    MeowerBot Bot Client!
    """

    Server = "wss://server.meower.org"
    APIURI = "https://api.meower.org"

    def __init__(self, username, password, logs=False):
        self.cl = Cloudlink()
        self.wss = self.cl.client(logs=logs, async_client=True)

        self.api = MeowerAPI(username)

        self.username = username
        self._psw = password
        self.authed = False
        self.BotID = None

        self.callbacks = {}

        self.internal_cbs = _bot_callbacks(self)

        self.wss.callback(self.wss.on_connect, self.internal_cbs._bot_on_connect)
        self.wss.callback(self.wss.on_close, self.internal_cbs._bot_on_close)
        self.wss.callback(self.wss.on_error, self.internal_cbs._bot_on_error)

        # Bind template callbacks
        self.wss.callback(self.wss.on_direct, self.internal_cbs._bot_on_direct)
        self.wss.callback(self.wss.on_ulist, self.internal_cbs._bot_on_ulist)
        self.wss.callback(
            self.wss.on_statuscode, self.internal_cbs._bot_handle_statuscode
        )
        self.wss.callback(self.wss.on_pvar, self.internal_cbs._bot_on_pvar)
        self.wss.callback(self.wss.on_pmsg, self.internal_cbs._bot_on_pmsg)

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

    def send_pmsg(self, msg, usr, lissener: str = None):
        """sends a pmsg"""
        self.wss.sendPrivateMessage(msg, username=usr, lissener=lissener)

    def send_pvar(self, name, val, usr, lissener: str = None):
        """sets a pvar on another client"""
        self.wss.sendPrivateVariable(name, val, username=usr, lissener=lissener)

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

    async def run(self):
        """Runs the bot!"""
        tasks = [asyncio.task]
        await self.wss.run(self.Server)
