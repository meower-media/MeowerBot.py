

class _Command:
	_bot = None
	def __init__(self, *args, name=None,  **kwargs):
		self._extra_args =  args
		self._extra_kwargs =  kwargs

		self.name = name
		self.func = None


	def __call__(self, func):
		self.func = func
		if self.name is None:
			self.name = self.func.__name__

		if self.name not in  self._bot.commands:
			self._bot.commands[self.name] = self

		return self.run_cmd

	def run_cmd(self, args, ctx):
		self.func(ctx, *args)

