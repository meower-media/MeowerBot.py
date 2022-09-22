# on_login

The callback that gets called when the bot is authed and connected to the server


## examples


```py
from MeowerBot import bot

YourBot = bot("username", "password")

...

async def on_login(bot=YourBot):
  print("Started")
  await YourBot.send_msg("Hello, World!")

...

YourBot.callback(on_login)

...

```