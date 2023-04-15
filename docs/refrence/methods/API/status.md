# MeowerAPI.status

This method gets the status of the meower.

## example

```py

from MeowerBot import Bot

bot = Bot()

def login(bot=bot):
	stats = bot.status()
	print(stats)

bot.callback(login, cbid="login") # when cbid is not specified it defaults to the function name (in this case "login")

```
