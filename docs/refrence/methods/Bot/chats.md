# Bot.enter_chat

This method sends the `user joined the chat!` message to the chat.


## args

- chat: str
  The chat you want to enter

  If not specified it defaults to "home"


## example

```py

from MeowerBot import Bot

bot = Bot()

@bot.command("enter")
def enter(bot=bot):
	bot.enter_chat("livechat")

```

# Bot.create_chat

This method creates a chat.

This is not well documented because it is not going to get used at at all.

## args

- chat_name: str
  The name of the chat


## example

```py

from MeowerBot import Bot

bot = Bot()

@bot.command("create")

def create(bot=bot):
	bot.create_chat("test")

```

This also fires the `chat_created` callback. However that is not documented, as its a raw packet.


