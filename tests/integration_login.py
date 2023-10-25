from MeowerBot import Bot
from MeowerBot.context import Context, Post
from MeowerBot.API import MeowerAPI
import asyncio
import logging
from os import environ as env

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("websockets.client").setLevel(level=logging.INFO)

bot = Bot()

@bot.event
async def login(t):
	print("Logged in!")

@bot.command(name="ping")
async def ping(ctx: Context):
	await ctx.send_msg("Pong!\n My latency is: " + str(bot.latency))

	

MeowerAPI.base_uri = "https://beta.meower.org/api/"

bot.run(env["uname"], env["pswd"], server="wss://beta.meower.org/api/v0/cloudlink") 

