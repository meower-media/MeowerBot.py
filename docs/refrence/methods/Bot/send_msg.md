#Bot.send_msg

Sends a message to the specified place if your bot has permission to do so.

## args

- message: str
  The message you want to send

- Keyword[default="home"] to: str
  The place you want to send the message to

  If not specified it defaults to "home"


## example

```py

from MeowerBot import Bot

bot = Bot()

def login(bot=bot):
	bot.send_msg("Hello World!", to="home")

bot.callback(login, cbid="login") # when cbid is not specified it defaults to the function name (in this case "login")

```
