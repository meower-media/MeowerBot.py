from .command import AppCommand, CB
import types
from typing import Any, Union


class Cog:
	commands: dict[str, AppCommand]
	callbacks: dict[str, list[types.CoroutineType]]

	__instence__: Union["Cog", None] = None

	def __init__(self) -> None:
		if isinstance(self.__instence__, Cog):
			return

		self.__class__.__instence__ = self
		self.commands = {}
		self.callbacks = {}
		self.update_commands()

	def update_commands(self):
		if not hasattr(self, "commands"):
			self.commands = {}

		if not hasattr(self, "callbacks"):
			self.callbacks = {}

		for command in self.__dir__():
			attr = getattr(self, command)
			if isinstance(attr, AppCommand):
				attr.register_class(self)
				self.commands = AppCommand.add_command(self.commands, attr)
			elif isinstance(attr, CB):
				self.callbacks[attr.id] = attr.func

	def __new__(cls, *args, **kwargs):
		if cls.__instence__ is None:
			self = super().__new__(cls)

			return self

		else:
			return cls.__instence__

__all__ = ["Cog"]
