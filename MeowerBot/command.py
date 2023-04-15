import warnings
import inspect


class AppCommand:
    connected = None

    def __init__(self, func, name=None, args=0):
        if name is None:
            name = func.__name__

        self.name = name
        self.func = func
        self.args = args

        self.arg_names = inspect.getfullargspec(func)[0]
        self.arg_types = func.__annotations__
        self.subcommands = {}

    def __call__(self, *args):
        raise RuntimeError("AppCommand is not callable")

    def register_class(self, con):
        self.connected = con

    def subcommand(self, name=None, args=0):
        def inner(func):

            cmd = AppCommand(func, name=name, args=args)
            cmd.register_class(self.connected)

            self.subcommands[name] = cmd.info()


            return func #dont want mb to register this as a root command

        return inner

    def run_cmd(self, ctx, *args):
        
        if self.subcommands and (args[0] if len(args) >= 1 else None) in self.subcommands:
            self.subcommands[args[0]]["command"].run_cmd(ctx, *args[1:])
            return
        
        if not self.args == 0:
            args = args[: self.args]

        if self.connected is None:
            self.func(ctx, *args)
        else:
            self.func(self.connected, ctx, *args)

    def info(self):
        return {
            self.name: {
                "args": self.args,
                "arg_names": self.arg_names,
                "arg_types": self.arg_types,
                "command": self,
                "func": self.func,

            }
        }


class _Command(AppCommand):
    def __init__(self, func, *args, name=None, **kwargs):
        super().__init__(func, *args, name=name, **kwargs)
        warnings.warn(
            "MeowerBot.command._Command has been renamed to MeowerBot.command.AppCommand"
        )


def command(name=None, args=0):
    def inner(func):

        cmd = AppCommand(func, name=name, args=args)

        return cmd

    return inner
