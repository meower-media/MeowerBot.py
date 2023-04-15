# MeowerAPI.statistics

This method gets the statistics of the meower DB. 

## example

```py

from MeowerBot import Bot

bot = Bot()

def login(bot=bot):
	stats = bot.statistics()
	print(stats)

bot.callback(login, cbid="login") # when cbid is not specified it defaults to the function name (in this case "login")

```
