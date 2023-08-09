from MeowerBot import Bot
from MeowerBot import cbids
from MeowerBot.context import CTX
import asyncio
import logging
from os import environ as env

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("websockets.client").setLevel(level=logging.INFO)

bot = Bot()

async def on_login(bot):
	print("Logged in!")


bot.callback(on_login, cbids.login)

@bot.command(aname="ping")
async def ping(ctx: CTX):
	await ctx.send_msg("Pong!\n My latency is: " + str(bot.latency))

async def main():
	await bot.run(env["uname"], env["password"])

asyncio.run(main())