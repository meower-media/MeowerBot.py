# on_statuscode

A callback that is called when the websocket gets a response from the server

This is most usefull with the lissener feture...

## examples

```py
from MeowerBot import bot

YourBot = bot("username", "password")

...

async def on_statuscode(code ,message , lissener=None, bot=YourBot):
  YourBot.statuscode = (code, message)
  
...

YourBot.callback(on_statuscode)

...

```