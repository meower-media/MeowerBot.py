
from MeowerBot import Bot, __version__
from MeowerBot.cog import Cog
from MeowerBot.command import command
from os import environ as env

from logging import basicConfig, DEBUG

basicConfig(level=DEBUG)
class MyBotCog(Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @command()
    def test2(self, ctx, *args):
        if not hasattr(self, "bot"):
            ctx.reply("No bot in cog")
            
        ctx.send_msg(" ".join(args))

bot = Bot(prefix="/")
cog = MyBotCog(bot)
bot.register_cog(cog)

@bot.command()
def test(ctx, *args):
	ctx.send_msg(" ".join(args) + "\n mb.py " + __version__)

bot.run(env['username'], env['password'])

