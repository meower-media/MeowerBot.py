<p align="center">
<h1> # Login Callback </h1>
</p>

This callback gets called when the bot has fully logged in

## args

### bot

A required keyword argument.

The bot object

## example

```py

from MeowerBot import Bot

...

bot = Bot()

...

def login(bot=bot):
   print(f"logged in as {bot.username} with prefix {bot.prefix}")

bot.callback(login)
```

