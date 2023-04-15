# Bot.run_command

Runs a command from a message.

Only use this if you have overridden the message callback.

## args

- msg: [Post](../types/Post.md)

## example

```py

from MeowerBot import Bot

bot = Bot()

def on_message(message, bot=bot):
	if message.user.username == bot.username: return
	if not message.data.startswith(bot.prefix): return

	message.data = message.data.split(bot.prefix, 1)[1]

	self.run_command(message)

bot.callback(on_message, cbid="message")

```
