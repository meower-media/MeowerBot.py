from MeowerBot import Bot


class DiscBotMeower(Bot):
    def __init__(self, prefix=None, autoreload: int or None = None):
        super().__init__(prefix, autoreload)

        self.callback(self.on_message, "message")
        self.callback(self.on_login, "login")
        self.callback(self.on_disconnect, "close")
        self.callback(self.on_error, "error")
        self.callback(self.on_raw_message, "raw_message")
        self.callback(self.on_pmsg, "pmsg")
        self.callback(self.on_ulist, "ulist")
        self.callback(self.on_statuscode, "statuscode")
        self.callback(self.on_chatlist, "chatlist")
        self.callback(self.on_raw_packet, "__raw__")

    async def on_message(self, msg):
        if ctx.user.username == self.username:
            return
        if not ctx.message.data.startswith(self.prefix):
            return

        ctx.message.data = ctx.message.data.split(self.prefix, 1)[1]

        await self.run_command(ctx.message)

    async def on_login(self):
        pass

    async def on_disconnect(self):
        pass

    async def on_error(self, err):
        pass

    async def on_raw_message(self, msg):
        pass

    async def on_pmsg(self, msg):
        pass

    async def on_ulist(self, ulist):
        pass

    async def on_statuscode(self, status, listener):
        pass

    async def on_chatlist(self, chatlist, listener):
        pass

    async def on_raw_packet(self, packet):
        pass

    def watch(self, event=None):
        def decorator(func):
            if event is None:
                event = func.__name__
            self.callback(func, event)
            return func
        return decorator

    def event(self, event=None):
        def decorator(func):
            if event is None:
                event = func.__name__
            setattr(self, event, func)
            return func
        return decorator
