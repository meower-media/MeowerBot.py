import inspect
from logging import getLogger
from typing import Any, Callable, Coroutine, Optional

logger = getLogger("MeowerBot")


class AppCommand:
	connected = None

	# noinspection PyShadowingNames
	@staticmethod
	def add_command(obj: dict, command: "AppCommand", ignore_subcommands: bool = True):
		if command.is_subcommand and ignore_subcommands:
			return obj

		for alias in command.alias + [command.name]:
			obj[alias] = command




		return obj


	def __init__(self, func, alias: Optional[list[str]] = None, name=None, args=0, is_subcommand=False): # type: ignore
		if name is None:
			name = func.__name__

		if alias is None:
			alias = []

		self.name = name
		self.func = func
		self.args_num = args
		self.alias = alias
		spec = inspect.signature(func)

		# Get the names and annotations of the arguments
		self.args = [
			(param.name, param.annotation)
			for param in spec.parameters.values()
			if param.name not in ["self", "ctx"]
		]

		# Check if the function has an arbitrary number of positional arguments
		self.has_unamed_args = any(
			param.kind == inspect.Parameter.VAR_POSITIONAL for param in spec.parameters.values()
		)

		self.is_subcommand = is_subcommand

		# Get the names, annotations, and default values of the keyword-only arguments
		self.optional_args = [
			(param.name, param.annotation, param.default)
			for param in spec.parameters.values()
			if param.kind == inspect.Parameter.KEYWORD_ONLY
		]

		# Set the namespace based on whether the command is a subcommand or not
		self.namespace = self.is_subcommand if type(self.is_subcommand) is str else self.name


		self.subcommands = {}

	def __call__(self, *args):
		raise RuntimeError("AppCommand is not callable")

	def register_class(self, con):
		self.connected = con

		for subcommand in self.subcommands.values():
			subcommand.register_class(con)



	def subcommand(self, name=None, args=0, aliases=None):
		def inner(func):

			cmd = AppCommand(func, name=name, args=args, alias=aliases)
			cmd.register_class(self.connected)

			self.subcommands = AppCommand.add_command(self.subcommands, cmd)

			return cmd # don't want mb to register this as a root command
		return inner

	async def run_cmd(self, ctx, *args) -> Optional[Exception]:

		try:
			# If a subcommand does not exist, ignore it,
			# so we can get the main command
			return await self.subcommands[args[0]].run_cmd(ctx, *args[1:])


		except (KeyError, IndexError):
			if self.subcommands is not {}:
				logger.error("Cannot find subcommand") # we don't have access to the bot here, so the best we can do it log it.

		if not self.args_num == 0:
			args = args[:self.args_num]

		try:
			if self.connected is None:
				await self.func(ctx, *args)
			else:
				await self.func(self.connected, ctx, *args)
		except Exception as e:
			return e

		return None


def command(name=None, args=0):
	def inner(func):

		cmd = AppCommand(func, name=name, args=args)

		return cmd

	return inner


class CB:
	def __init__(self, func, id):
		self.func = func
		self.id = id



def callback(callback_id: str) -> Callable:
	def inner(func: Callable) -> CB:
		return CB(func, callback_id)
	return inner

__all__ = ["callback", "CB", "command", "AppCommand"]
