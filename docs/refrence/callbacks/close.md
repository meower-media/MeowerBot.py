<p align="center">
<h1>Close callback</h1>
</p>

This callback gets called when websocket for the bot is closed.

## Arguments
   - bot: MeowerBot.Bot

## Example Code

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


