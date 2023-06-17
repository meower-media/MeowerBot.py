
from MeowerBot import Bot, __version__
from MeowerBot.command import AppCommand
from MeowerBot.ext.help import Help

from os import environ as env
from logging import basicConfig, DEBUG

basicConfig(level=DEBUG)

bot: Bot = Bot(prefix="!", autoreload=1)

test: AppCommand

@bot.command()
def test(ctx, *args):
	ctx.send_msg(" ".join(args) + "\n mb.py " + __version__)

@test.subcommand()
def sub(ctx, *args):
	ctx.send_msg(" ".join(args))
	

@bot.command(args=0)
def reloadtime(ctx):
	ctx.send_msg(f"My reload time is {round(bot.autoreload_time)}" )

help = Help(bot)


bot.register_cog(help)
help.generate_help()
print(help.pages)
bot.run(env['uname'], env['password'])

