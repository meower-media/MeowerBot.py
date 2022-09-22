# on_pvar

gets called when someone sends you a private var

## examples


```py
from MeowerBot import bot

YourBot = bot("username", "password")

...

async def on_pvar(var,content,origin,bot=YourBot):
  setattr(YourBot, var, content)

...

YourBot.callback(on_pvar)

...

```