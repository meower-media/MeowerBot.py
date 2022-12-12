
from MeowerBot import Bot, __version__
from MeowerBot.cog import Cog
from MeowerBot.command import command
from os import environ as env


class MyBotCog(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command()
    def test(self, ctx, *args):
        ctx.send_msg(" ".join(args))

bot = Bot(debug=True, prefix="/" + "\n mb.py " + __version__)

@bot.command()
def test(ctx, *args):
	ctx.send_msg(" ".join(args) + "\n mb.py " + __version__)

bot.run(env['username'], env['password'])

