
from MeowerBot import Bot, __version__
from os import environ as env


bot = Bot(debug=True, prefix="/")

@bot.command()
def test(ctx, *args):
	ctx.send_message(" ".join(args) + "\n mb.py " + __version__)

bot.run(env['username'], env['password'])

