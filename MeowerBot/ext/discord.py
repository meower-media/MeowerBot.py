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


	def on_message(self, msg):
        if ctx.user.username == self.username:
            return
        if not ctx.message.data.startswith(self.prefix):
            return

        ctx.message.data = ctx.message.data.split(self.prefix, 1)[1]

        self.run_command(ctx.message)

	def on_login(self):
		pass

	def on_disconnect(self):
		pass

	def on_error(self, err):
		pass

	def on_raw_message(self, msg):
		pass

	def on_pmsg(self, msg):
		pass

	def on_ulist(self, ulist):
		pass

	def on_statuscode(self, status, listener):
		pass

	def on_chatlist(self, chatlist, listener):
		pass

	def on_raw_packet(self, packet):
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