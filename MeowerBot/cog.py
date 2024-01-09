import types
from typing import Union

from .command import AppCommand, CB
from typing import Dict
from types import CoroutineType

class Cog:
	commands: dict[str, AppCommand]
	callbacks: dict[str, CoroutineType]

	__instance__: Union["Cog", None] = None

	def __init__(self) -> None:
		if isinstance(self.__instance__, Cog):
			return

		self.__class__.__instance__ = self
		self.commands = {}
		self.callbacks: Dict[str, CoroutineType] = {}
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
		if cls.__instance__ is None:
			self = super().__new__(cls)

			return self

		else:
			return cls.__instance__

__all__ = ["Cog"]
