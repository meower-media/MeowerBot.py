from MeowerBot import Bot
from MeowerBot import cbids
from MeowerBot.context import CTX, Post
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

	def predicate(msg: Post):
		return ctx.user.username == msg.user.username and msg.chat == ctx.message.chat

	msg = await bot.wait_for_message(predicate, timeout=100)
	await ctx.send_msg("You said: " + str(msg))
async def main():
	await bot.run(env["uname"], env["password"])

asyncio.run(main())