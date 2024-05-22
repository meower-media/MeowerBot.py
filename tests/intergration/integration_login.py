from typing import List

from MeowerBot import Bot, CallBackIds
from MeowerBot.context import Context, PartialUser, Post, User
from MeowerBot.cog import Cog
from MeowerBot.command import command

import logging

from dotenv import load_dotenv  # type: ignore

from os import environ as env
from MeowerBot.ext.help import Help as HelpExt

load_dotenv()  # type: ignore

logging.basicConfig(
	level=logging.DEBUG,
	handlers=[
		logging.FileHandler("debug.log", encoding='utf8'),
		logging.StreamHandler()
	]
)

logging.getLogger("websockets.client").setLevel(logging.INFO)
bot = Bot()


@bot.event
async def login(_token):
	print("Logged in!")


@bot.command(name="ping")
async def ping(ctx: Context):
	await ctx.send_msg("Pong!\n My latency is: " + str(bot.latency))


# noinspection PyIncorrectDocstring
@bot.command(name="logs")
async def get_logs(ctx: Context, *args):
	"""
	Arguments:
		start: Optional[int]
		end: Optional[int]

	Formated like this:
		start=...

	@prefix get_logs start=-200 end=-1
	"""
	# start=...
	# end=...
	start = -10
	end = -1
	arg: str
	for arg in args:
		if arg.startswith("start"):
			start = int(arg.split("=")[1])
		elif arg.startswith("end"):
			end = int(arg.split("=")[1])

	with open("debug.log") as logfile:
		logs = logfile.readlines()

	message = await ctx.send_msg("".join(logs[start: end]))
	if not message:
		await ctx.reply("Error: Logs to big for current env")


@bot.command(name="bots")
async def get_bots(ctx: Context):
	await ctx.reply(f"\n {" ".join(list(bot.cache.bots.keys()))}")


@ping.subcommand(name="pong")
async def pong(ctx: Context, *message: str):
	await ctx.send_msg(f"Pong!{" ".join(message)}")


class Ping(Cog):
	def __init__(self, _bot: Bot):
		super().__init__()
		self._bot = _bot

	@command()
	async def cog_ping(self, ctx: Context):
		await ctx.send_msg("Pong!\n My latency is: " + str(self._bot.latency))
		print(bot.api.headers.get("token"))

	@cog_ping.subcommand()
	async def ping(self, ctx: Context):
		await ctx.send_msg("Pong!\n My latency is: " + str(self._bot.latency))


@bot.event
async def login(token):
	assert await bot.get_chat("9bf5bddd-cd1a-4c0d-a34c-31ae554ed4a7").fetch() is not None
	assert await bot.get_chat("9bf5bddd").fetch() is None
	assert await PartialUser(bot.user.username, bot).fetch() is not None
	assert await PartialUser("A" * 21, bot).fetch() is None

@bot.event
async def ulist(userlist: List[User]):
	assert type(userlist[0]) is User

@bot.listen(CallBackIds.message)
async def on_message(message: Post):
	assert isinstance(message, Post)
	assert isinstance(bot.get_context(message), Context)

bot.register_cog(Ping(bot))
bot.register_cog(HelpExt(bot, disable_command_newlines=True))
bot.run(env["uname"], env["pswd"])
