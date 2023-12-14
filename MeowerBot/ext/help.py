import inspect

from MeowerBot.cog import Cog
from MeowerBot.command import AppCommand, callback, command
from MeowerBot import CallBackIds


def _get_index_or(lst, i, d):
	try:
		r = lst[i]
		if str(r) == "":
			return d
		return r.__name__
	except IndexError:
		return d


class Help(Cog):
	__instance__: "Help"
	_generated: bool = False

	def __init__(self, bot, disable_command_newlines=False, *args, **kwargs):
		Cog.__init__(self)
		self.bot = bot
		self.page = ""
		self.pages = []
		self.disable_command_newlines = disable_command_newlines




	def generate_help(self):
		if self.bot.prefix == f"@{self.bot.username}":
			self.bot.prefix = f"@{self.bot.username} "

		self.pages = []
		self.page = ""
		page_size = 0
		for name, cog in self.bot.cogs.items():

			self.page += f"-- [ {name} ] -- \n "
			page_size = len(self.page)

			for command in cog.commands.values(): # noqa
				self.handle_command(command.name, command)

				if page_size >= 500:
					self.pages.append(self.page)
					self.page = f"-- [ {name} ] -- \n "
					page_size = len(self.page)

		self.page += "-- [ Unsorted ] -- \n  "
		page_size = len(self.page)



		for name, comamnd in self.bot.commands.items():
			if comamnd.connected is not None:
				continue # skip cog based commands

			self.handle_command(name, comamnd)

			if page_size >= 500:
				self.pages.append(self.page)
				self.page = f"-- [ Unsorted ] -- \n " # noqa
				page_size = len(self.page)

		self.pages.append(self.page)

		if self.bot.prefix == f"@{self.bot.username} ":
			self.bot.prefix = f"@{self.bot.username}"


	def handle_command(self, name, cmd: AppCommand):
		self.page += f"{self.bot.prefix}{name} "

		for arg in cmd.args:
			self.page += f"<{arg[0]}: {str(_get_index_or(arg, 1, 'any'))}> "


		for arg in cmd.optional_args:
			self.page += f"[{arg[0]}: {str(_get_index_or(arg, 1, 'any'))}: optional ] "

		if cmd.func.__doc__ is not None:
			self.page += f"\n\t{cmd.func.__doc__}"



		self.page += " \n "

		for subcommand_name, command in cmd.subcommands.items(): # noqa
			self.page += f" \t" # noqa
			self.handle_command(f"{name} {subcommand_name}", command)
			if not self.disable_command_newlines:
				self.page += " \n "

		self.page += " \n "

	@command(name="help")
	async def help(self, ctx, page: int = 0):

		if page >= len(self.pages):
			page = len(self.pages) - 1

		await ctx.send_msg(self.pages[page])

	@callback(CallBackIds.login)
	@staticmethod
	async def _login(token):
		self = Help.__instance__
		assert self is not None
		if self._generated:
			return

		self._generated = True
		self.bot.logger.info("Generating Help")
		self.generate_help() # generate help on login, bugfix for default prefix, and people being dumb
