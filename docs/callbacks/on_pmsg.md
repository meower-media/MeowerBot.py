# on_pmsg

gets called when someone sends you a private msg

## examples


```py
from MeowerBot import bot

YourBot = bot("username", "password")

...

async def on_pmsg(content,origin,bot=YourBot):
  print(f"got pmsg from {origin}: {content}")

...

YourBot.callback(on_pmsg)

...

```