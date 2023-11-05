# MeowerBot.py

A bot library made for [Meower](https://github.com/meower-media-co/)


## License

see [LICENSE](./LICENSE)


## docs

Currently, there is no documentation as a full rewrite just happened.




## Quick Example

```py
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

bot.register_cog(HelpExt(bot))
bot.run(env["uname"], env["pswd"])
```

That example may be outdated. if it is outdated, the correct version is in [here](./tests/intergration/integration_login.py)

There are extra examples [here](./tests/intergration/)