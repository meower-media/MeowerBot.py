from MeowerBot.cog import Cog
from MeowerBot.command import command, AppCommand, callback
from MeowerBot import cbids
import inspect


def _get_index_or(lst, i, d):
	try:
		r = lst[i]
		if str(r) == str(inspect._empty):
			return d
		return r.__name__
	except IndexError:
		return d


class Help(Cog):
	__instence__: "Help"

	def __init__(self, bot, *args, **kwargs):
		Cog.__init__(self)
		self.bot = bot
		self.page = ""
		self.pages = []




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
		self.page += (f"{self.bot.prefix}{name} ")

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
			self.page += " \n "

		self.page += " \n "

	@command(name="help")
	async def help(self, ctx, page: int = 0):

		if page >= len(self.pages):
			page = len(self.pages) - 1

		await ctx.send_msg(self.pages[page])

	@callback(cbids.login)
	@staticmethod
	async def _login(token):
		self = Help.__instence__
		assert self is not None

		self.bot.logger.info("Generating Help")
		self.generate_help() # generate help on login, bugfix for default prefix and people being dumb
