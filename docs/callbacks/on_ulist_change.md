# on_ulist_change


Gets called when the server sends a ulist

## examples

```py
from MeowerBot import bot

YourBot = bot("username", "password")

...

async def on_ulist_change(ulist, bot=YourBot):
  print(f"Got New Ulist! \n {"\n".join(ulist)}")

...

YourBot.callback(on_ulist_change)

...

```