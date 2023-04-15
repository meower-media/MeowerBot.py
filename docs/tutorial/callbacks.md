# MeowerBot callbacks

A callback is a function that gets called when a certain event happens.

That makes it so you can recieve events from Meower, and do stuff with them.


## Login callback
This callback is for when the bot logs in. You can use it, for example, to send a message on startup or run a local command. If the bot fails to login, this callback will not be called.

There is more info on the login callback [here](../refrence/callbacks/login.md)

### Example code

```py
from MeowerBot import Bot

bot = Bot()

def login(bot=bot):
	print("Logged in!")

bot.callback(login, cbid="login") # If the cbid is not specifed, it will use the function name

```

## Error Callback

This callback is for when an error happens. It is used for sending a message when an error happens, or for logging errors (However MeowerBot.py already logs errors, so you don't need to do that) 

There is more info on the error callback [here](../refrence/callbacks/error.md)

### Arguments

- e: Exception
	- The error that caused this callback to be called

### Example code

```py
from MeowerBot import Bot

bot = Bot()

def error(e, bot=bot):
	print(e)

bot.callback(error, cbid="error") # If the cbid is not specifed, it will use the function name

```

## Close callback

This callback gets called when the websocket for the bot is fully closed and the bot is no longer connected to Meower. The only way to send a message after this callback is called is to reconnect the bot or use `https://webhooks.meower.org/post/home` to send a message.

There is more info on the close callback [here](../refrence/callbacks/close.md)

### Example code

```py
from MeowerBot import Bot

bot = Bot()

def close(bot=bot):
	print("Bye!")

bot.callback(close, cbid="close") # If the cbid is not specifed, it will use the function name

```

## Message callback

This callback is called when a message is sent in a place the bot can see. This includes home, livechat and group chats that the bot has been added to.

There is more info on the message callback [here](../refrence/callbacks/message.md)

Although be warned, the default implementation is disabled when this callback is added, so you will need to do that yourself.



### Arguments

- message: MeowerBot.Message
	- The message that was sent


### Example code

```py
from MeowerBot import Bot

bot = Bot()

def message(message, bot=bot):
	"""This is the default implementation of the message callback, slightly modified to work without subclassing"""

    if ctx.user.username == bot.username:
        return
    if not ctx.message.data.startswith(bot.prefix):
        return

    ctx.message.data = ctx.message.data.split(bot.prefix, 1)[1]

    bot.run_command(ctx.message)

bot.callback(message, cbid="message") # If the cbid is not specifed, it will use the function name

```

## Cloudlink Packet callback

This callback gets called when a message is sent. However this time it is a raw packet, and not a message object. Good for MeowerBot.py 1.x.x enjoyers.

There is more info on the cloudlink packet callback [here](../refrence/callbacks/raw.md)

### Argumentx

- message: dict[str, any]
	- The packet that was recieved

	```python
		{
	        "type": 1,
            "post_origin": str(post_origin), 
            "u": str(user), 
            "t": timestamp, 
            "p": str(content),
            "post_id": post_id, 
		}
	```

### Example code

```py
from MeowerBot import Bot

bot = Bot()

def raw_msg(message, bot=bot):
	print(f"{message['u']}: {message['p']}")

bot.callback(raw_msg, cbid="__raw__") # If the cbid is not specifed, it will use the function name

```



