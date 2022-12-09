from abc import ABCMeta, abstractmethod

        

class Cog(metaclass=ABCMeta):
    instence = None
    _Cog_commands = None

    def __new__(cls):
        if cls.instence is None:
            cls.instence = super().__new__(cls)
        return cls.instence

    @classmethod
    def __subclasshook__(cls):
        cls._Cog_commands = {} # to make cogs not share cmds

    @classmethod
    def register_command(cls, command):
        cls._Cog_commands[command.name] = command
    
    
    def get_commands(self):
        for cmd in self._Cog_commands:
            cmd.func = getattr(self, cmd.func.__name__) # binding self 
        
        return self._Cog_commands

    