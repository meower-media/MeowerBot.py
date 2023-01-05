<p align="center">
<h1> close callback </h1>
</p>

This callback gets called when the bot`s wss closes

## args

### bot

A required keyword argument

The bot object

## example

```py

from MeowerBot import Bot

...
bot = Bot()

...

def close(bot=bot):
   print("Bye")

bot.callback(close)

...

```


