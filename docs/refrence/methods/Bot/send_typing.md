# Bot.send_typing

Sends a typing indicator to the specified place if your bot has permission to do so.

## args

- Keyword[default="home"] to: str
  The place you want to send the typing indicator to

  If not specified it defaults to "home"


## example

```py

from MeowerBot import Bot
import time

bot = Bot()

def login(bot=bot):
	while True:
		bot.send_typing(to="home")
		time.sleep(1)

bot.callback(login, cbid="login") # when cbid is not specified it defaults to the function name (in this case "login")

```