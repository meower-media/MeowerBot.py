from .command import AppCommand, command
import weakref


class Cog:
    commands = None
    __instence__ = None

    def __init__(self) -> None:
        if isinstance(self.__instence__, Cog):
            return
            

        self.__class__.__instence__ = self
        commands = {}

        
        for command in self.__dir__():
            attr = getattr(self, command)
            if isinstance(attr, AppCommand):
                attr.register_class(self)
                commands.update(attr.info())
        self.commands = commands

    def update_commands(self):
        for command in self.__dir__():
            attr = getattr(self, command)
            if isinstance(attr, AppCommand):
                self.commands = AppCommand.add_command(self.commands, attr)

    def __new__(cls, *args, **kwargs):
        if cls.__instence__ is None:
            self = super().__new__(cls)

            return self

        else:
            return cls.__instence__

    def get_info(self):
        return self.__commands__
