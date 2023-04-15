# Bot.login

This is the method that logs your bot in.

This method blocks the main thread for the duration of the bot being online.

## args

	- username: str
		The username of the bot

	- password: str
		The password of the bot

	- Keyword[optional] server: str = "https://server.meower.org/"
		The server to connect to


## example

```py
from MeowerBot import Bot

bot = Bot()

bot.login("username", "password")
```

or using python-dotenv

```py
from MeowerBot import Bot
from dotenv import load_dotenv
import os

from os import environ as env


load_dotenv(overide=os.name == "nt") # if you are on windows, you need to overide the env vars because dotenv is stupid and does not overide the username var

bot = Bot()

bot.login(env["username"], env["password"])
```

```dotenv
username=
password=
```

