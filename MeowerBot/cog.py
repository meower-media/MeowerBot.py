from .command import AppCommand
import weakref

class Cog:
    __commands__ = None
    __instence__ = None

    def __new__(cls):
        if cls.__instence__ is None:
            self = super().__new__(cls)

            cls.__instence__ = self
            self.__commands__ = {}

            for command in self.__dict__.items():
                if isinstance(command, AppCommand):
                  command.register_class(weakref.ref(self))
                  self.__commands__.update(command.info())

            return self

        else:
            return cls.__instence__

    def info(self):
        return self.__commands__
