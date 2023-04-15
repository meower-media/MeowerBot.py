# Bot.callback

This method adds a callback to the bot. 

This is also not a decorator.

## args

- cb: function
  The callback function

- Keyword[optional] cbid: str
  The id of the callback

  If not specified it defaults to the function name

## example

```py
from MeowerBot import Bot

bot = Bot()

def login(bot=bot):
	print(f"logged in as {bot.username} with prefix {bot.prefix}")

bot.callback(login, cbid="login") # when cbid is not specified it defaults to the function name (in this case "login")

```
