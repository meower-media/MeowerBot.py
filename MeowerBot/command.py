import warnings
import inspect
import traceback
from logging import getLogger

logger = getLogger("MeowerBot")


class AppCommand:
    connected = None

    def __init__(self, func, name=None, args=0, is_subcommand=False):
        if name is None:
            name = func.__name__

        self.name = name
        self.func = func
        self.args_num = args

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



    def subcommand(self, name=None, args=0):
        def inner(func):

            cmd = AppCommand(func, name=name, args=args)
            cmd.register_class(self.connected)

            self.subcommands.update(cmd.info())


            return func #dont want mb to register this as a root command
        return inner
    

    def run_cmd(self, ctx, *args):
        
        try:
            self.subcommands[args[0]]["command"].run_cmd(ctx, *args[1:])
            return
        except KeyError:
            #print(f"KeyError: {args}")
            #print(f"Subcommands: {self.subcommands}")
            logger.debug(f"Cant find subcommand {args[0]}")

        except IndexError:
            logger.debug(traceback.format_exc())
        
        if not self.args_num == 0:
            args = args[:self.args_num]

        if self.connected is None:
            self.func(ctx, *args)
        else:
            self.func(self.connected, ctx, *args)

    def info(self):
        return {
            self.name: {
                "args": self.args,
                "args_num": self.args_num,
                "optional_args": self.optional_args,
                "has_unamed_args": self.has_unamed_args,
                "subcommands": self.subcommands,
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
