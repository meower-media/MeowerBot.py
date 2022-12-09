
from MeowerBot import Bot, __version__
from MeowerBot.commands import command
from MeowerBot.cogs import Cog

from os import environ as env

class BotCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    def test2(ctx, *args):
       ctx.send_msg(" ".join(args) + "\n mb.py " + __version__)


bot = Bot(debug=True, prefix="/")

@command()
def test(ctx, *args):
	ctx.send_msg(" ".join(args) + "\n mb.py " + __version__)


bot.register_cog(BotCog(bot))

bot.run(env['username'], env['password'])

