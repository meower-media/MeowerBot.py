from logging import DEBUG, basicConfig
from os import environ as env

from MeowerBot import Bot, __version__
from MeowerBot.command import AppCommand

basicConfig(level=DEBUG)

bot: Bot = Bot(prefix="/", autoreload=1)

test: AppCommand


@bot.command()
def test(ctx, *args):
    ctx.send_msg(" ".join(args) + "\n mb.py " + __version__)


@test.subcommand()
def sub(ctx, *args):
    ctx.send_msg(" ".join(args))


@bot.command(args=0)
def reloadtime(ctx):
    ctx.send_msg(f"My reload time is {round(bot.autoreload_time)}")


bot.run(env["uname"], env["password"])
