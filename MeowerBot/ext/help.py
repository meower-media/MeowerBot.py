from MeowerBot.cog import Cog
from MeowerBot.command import command
import inspect

def _get_index_or(l, i, d):
	try:
		r = l[i]
		if str(r) == str(inspect._empty):
			return d
		return r
	except IndexError:
		return d

class Help(Cog):
	def __init__(self, bot, *args, **kwargs):
		self.bot = bot
		self.page = ""
		Cog.__init__(self)

		

	def generate_help(self):
		self.pages = []
		self.page = ""
		page_size = 0
		for name, cog in self.bot.cogs.items():

			self.page+= f"-- [ {name} ] --\n"
			page_size = len(self.page)

			for command in cog.__commands__.values():
				self.handle_command(command["command"].name, command["command"])

				if page_size >= 500:
					self.pages.append(page)
					self.page = f"-- [ {name} ] --\n"
					page_size = len(self.page)
		
		self.page += "-- [ Unsorted ] --\n"
		page_size = len(self.page)

	
		
		for name, comamnd in self.bot.commands.items():
			if comamnd["command"].connected is not None: continue #skip cog based commands

			self.handle_command(name, comamnd["command"])

			if page_size >= 500:
				self.pages.append(page)
				self.page = f"-- [ Unsorted ] --\n"
				page_size = len(self.page)

		self.pages.append(self.page)

	
	def handle_command(self, name, cmd):
		self.page += (f"{self.bot.prefix}{name} ")

		for arg in cmd.args:
			self.page += f"<{arg[0][0]}: {str(_get_index_or(arg, 1, 'any'))}> "

		
		for arg in cmd.optional_args:
			self.page += f"[{arg[0]}: {str(_get_index_or(arg, 1, 'any'))}: optional ] "
		
		self.page += "\n"

		for subcommand_name, command in cmd.subcommands.items():
			self.page += f"\t"
			self.handle_command(f"{name} {subcommand_name}", command["command"])
			self.page += "\n"
		
		self.page += "\n"

	@command(name="help")
	def help(self, ctx, page: int=0):

		if page >= len(self.pages):
			page = len(self.pages) - 1
		
		ctx.send_msg(self.pages[page])

		