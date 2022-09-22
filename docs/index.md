# MeowerBot.py

MeowerBot.py is a bot lib for meower. It is the original Major Bot lib for meower.

## Starter Code

```py
from MeowerBot import bot
from asyncio import run

YourBot = bot("username", "password")

async def on_raw_msg(msg, lissener=None, bot=YourBot):
  print(f"{msg['u']}: {msg['p']}")

  if not msg['u'] == YourBot.username:
    await YourBot.send_msg("got the msg", where=msg['post_origin'])

YourBot.callback(on_raw_msg)

YourBot.start() #Not Implememented til cl4 server is impl
```