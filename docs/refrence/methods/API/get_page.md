# MeowerApi.get_page

This method gets a page of messages from the API. 

Does not convert the messages to Message objects

## args

- page: int
  The page you want to get

  If not specified it defaults to 1

- chatid: str
  The chat you want to get the messages from

  If not specified it defaults to "home"


## example

```py

from MeowerBot import Bot

bot = Bot()

def login(bot=bot):
	for msg in bot.get_page(1, "home")['autoget']:
		print(f"{msg['u']}: {msg['p']})

bot.callback(login, cbid="login") # when cbid is not specified it defaults to the function name (in this case "login")

```

