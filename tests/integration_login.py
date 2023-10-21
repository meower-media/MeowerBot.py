from MeowerBot import Bot
from MeowerBot.context import Context, Post
from MeowerBot.API import MeowerAPI
import asyncio
import logging
from os import environ as env

logging.basicConfig(level=logging.DEBUG)
#logging.getLogger("websockets.client").setLevel(level=logging.INFO)

bot = Bot()

@bot.event
async def login(t):
	print("Logged in!")

@bot.command(name="ping")
async def ping(ctx: Context):
	await ctx.send_msg("Pong!\n My latency is: " + str(bot.latency))

	def predicate(msg: Post):
		return ctx.user.username == msg.user.username and msg.chat == ctx.message.chat

	msg = await bot.wait_for_message(predicate, timeout=100)
	await ctx.send_msg("You said: " + str(msg))

MeowerAPI.base_uri =  "http://beta.meower.org:5174/api/"

bot.run(env['uname'], env['password'], server="wss://beta.meower.org/api/v0/cloudlink")

