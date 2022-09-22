# on_raw_msg

A callback that is called when the websocket gets a packet that has the keys

```json
{
  "val":{"post_origin":"home"}
}
```

it includes everything sent to the bot by the server

The most usefull keys are `p`  (post) `u` (username) and `post_origin`

## examples

```py
from MeowerBot import bot

YourBot = bot("username", "password")

...

async def on_raw_msg(msg, lissener=None, bot=YourBot):
  print(f"{msg['u']}: {msg['p']}")

  if not msg['u'] == YourBot.username:
    await YourBot.send_msg("got the msg", where=msg['post_origin'])

...

YourBot.callback(on_raw_msg)

...

```