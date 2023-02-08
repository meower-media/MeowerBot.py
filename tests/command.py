
from MeowerBot import Bot, __version__
from os import environ as env
from logging import basicConfig, DEBUG

basicConfig(level=DEBUG)

bot: Bot = Bot(prefix="/", autoreload=1)

@bot.command()
def test(ctx, *args):
	ctx.send_msg(" ".join(args) + "\n mb.py " + __version__)

@bot.command(args=0)
def reloadtime(ctx):
	ctx.send_msg(f"My reload time is {round(bot.autoreload_time)}" )
	
bot.run(env['username'], env['password'])

