<p align="center">
<h1>Login Callback </h1>
</p>

This callback gets called when the bot has fully logged in.

## Arguments

### bot

A required keyword argument.

The bot object

## Example code

```py

from MeowerBot import Bot

...

bot = Bot()

...

def login(bot=bot):
   print(f"logged in as {bot.username} with prefix {bot.prefix}")

bot.callback(login, cbid="login") # when cbid is not specified it defaults to the function name (in this case "login")
```

