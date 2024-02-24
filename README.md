<p align="center">
  <img src="https://raw.githubusercontent.com/meower-community/MeowerBot.py/master/assets/logo.svg"/>
</p>

A Python Bot library with an API like nextcord or discord.py, but instead of discord, it is made for the FOSS Social media [Meower](https://github.com/meower-media-co/)



## Installing

```bash
pip install MeowerBot
```

## Examples

```py
from MeowerBot import Bot, CallBackIds
from MeowerBot.context import Context, Post
from MeowerBot.cog import Cog
from MeowerBot.command import command

import logging

from dotenv import load_dotenv # type: ignore

load_dotenv() # type: ignore

from os import environ as env
from MeowerBot.ext.help import Help as HelpExt

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
	def __init__(self, bot: Bot):
		super().__init__()
		self.bot = bot

	@command()
	async def cog_ping(self, ctx: Context):
		await ctx.send_msg("Pong!\n My latency is: " + str(self.bot.latency))
		print(bot.api.headers.get("token"))
	@cog_ping.subcommand()
	async def ping(self, ctx: Context):
		await ctx.send_msg("Pong!\n My latency is: " + str(self.bot.latency))





bot.register_cog(Ping(bot))
bot.register_cog(HelpExt(bot, disable_command_newlines=True))
bot.run(env["uname"], env["pswd"])

``` 

That example may be outdated.  
(Updated as of 1/8/2024 CT)
If it is outdated, the place where it is taken from is [the login test](./tests/intergration/integration_login.py)

## Extra links

There are extra examples [in the intergration tests](./tests/intergration/)
The docs are located on my domain made with sphinx. They are located [here](https://meowerbot.showierdata.xyz/)
MeowerBot.py's [MIT LICENSE](./LICENSE)
