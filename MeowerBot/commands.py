import functools
from .Bot import Bot

class _Command:
    _bot = None
    def __init__(self, func, name, arg_count):
        self.name = name
        self.func = func
        self.arg_count = arg_count


    def run_cmd(self, args, ctx):
        if self.arg_count == 0:
            self.func(ctx, *args)
            return
        self.func(ctx, *args[:self.arg_count])

def command(name=None, arg_count=0, bot=None):
    def inner(func):
        @functools.wraps(func)
        def callfunc(*args, **kwargs):
            raise NotImplementedError("This Should Never be called\n it should disapear")
        
        cmd = _Command(func, name, arg_count)

        if hasattr(func, "__class__"):
            func.__class__.register_command(cmd)
        elif bot is not None:
            bot.commands[cmd.name] = cmd
        else:
            Bot.register_command(cmd)


        return callfunc

