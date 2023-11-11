from MeowerBot import Bot
from MeowerBot.context import Context

import logging

from dotenv import load_dotenv # type: ignore

load_dotenv() # type: ignore

from os import environ as env
from MeowerBot.ext.help import Help as HelpExt

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("websockets.client").setLevel(level=logging.INFO)

bot = Bot()


@bot.event
async def login(t):
	print("Logged in!")


@bot.command(name="ping")
async def ping(ctx: Context):
	await ctx.send_msg("Pong!\n My latency is: " + str(bot.latency))

bot.register_cog(HelpExt(bot, disable_command_newlines=True))
bot.run(env["uname"], env["pswd"])
