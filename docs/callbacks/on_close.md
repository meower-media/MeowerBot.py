# on_close

The callback that gets called when the bot wss is fully closed.


## examples


```py
from MeowerBot import bot

YourBot = bot("username", "password")

...

async def on_close(bot=YourBot):
  print("Goodbye, Closeing")

...

YourBot.callback(on_close)

...

```