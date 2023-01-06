from .command import AppCommand
import weakref


class Cog:
    __commands__ = None
    __instence__ = None

    def __init__(self) -> None:
        self.__class__.__instence__ = self
        commands = {}

        for command in self.__dir__():
            attr = getattr(self, command)
            if isinstance(attr, AppCommand):
                attr.register_class(self)
                commands.update(attr.info())
        self.__commands__ = commands

    def __new__(cls, *args, **kwargs):
        if cls.__instence__ is None:
            self = super().__new__(cls)

            return self

        else:
            return cls.__instence__

    def get_info(self):
        return self.__commands__
