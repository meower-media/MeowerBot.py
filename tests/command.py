
from MeowerBot import Bot, __version__
from os import environ as env
from logging import basicConfig, DEBUG

basicConfig(level=DEBUG)

bot: Bot = Bot(prefix="/")

@bot.command()
def test(ctx, *args):
	ctx.send_msg(" ".join(args) + "\n mb.py " + __version__)

bot.run(env['username'], env['password'])

