<p align="center">
<h1> callback message </h1>
</p>

The callback `message` is the gateway into making your own prefix style/ ban system

##  arguments

- msg: [Post](../types/Post.md)
    This object is a Post object containing everything the post has to offer


## example

```py
from MeowerBot import Bot
...

...
bot = Bot()
...

def on_message(message, bot=bot):
    if message.user.username == bot.username: return
    if not message.data.startswith(bot.prefix): return

    message.data = message.data.split(bot.prefix, 1)[1]


    self.run_command(message)

bot.callback(on_message, cbid="message")

...
```