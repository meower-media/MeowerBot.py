# MeowerBot callbacks

A callback is a function that gets called when a certain event happens.

That makes it so you can recieve events from meower, and do stuff with them.


## the login callback

This callback is for when the bot logs in. You can use it to do stuff like send a message on startup. However if the bot fails to login, this callback will not get called.

There is more info on the login callback [here](../refrence/callbacks/login.md)

### an example

```py
from MeowerBot import Bot

bot = Bot()

def login(bot=bot):
	print("Logged in!")

bot.callback(login, cbid="login") # If the cbid is not specifed, it will use the function name

```

## the error callback

This callback is for when an error happens. It is used for sending a message when an error happens, or for logging errors (However MeowerBot.py already logs errors, so you don't need to do that) 

There is more info on the error callback [here](../refrence/callbacks/error.md)

### arguments

- e: Exception
	- The error that caused this callback to get called

### an example

```py
from MeowerBot import Bot

bot = Bot()

def error(e, bot=bot):
	print(e)

bot.callback(error, cbid="error") # If the cbid is not specifed, it will use the function name

```

## the close callback

This callback gets called when the websocket is fully closed, and the bot is no longer connected to meower. The only way to send a message after this callback is called is to reconnect the bot, or use `https://webhooks.meower.org/post/home` to send a message.

There is more info on the close callback [here](../refrence/callbacks/close.md)

### an example

```py
from MeowerBot import Bot

bot = Bot()

def close(bot=bot):
	print("Bye!")

bot.callback(close, cbid="close") # If the cbid is not specifed, it will use the function name

```

## the message callback

This callback gets called when a message is sent in a place the bot can see. This includes home, and livechat.

There is more info on the message callback [here](../refrence/callbacks/message.md)

Although be warned, the default implementation is desabled when this callback is added, so you will need to do that yourself.



### arguments

- message: MeowerBot.Message
	- The message that was sent


### an example

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

## The cloudlink packet callback. 

This callback gets called when a message is sent. However this time it is a raw packet, and not a message object. Good for mb.py 1.0.0 enjoyers.

There is more info on the cloudlink packet callback [here](../refrence/callbacks/raw.md)

### arguments

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

### an example

```py
from MeowerBot import Bot

bot = Bot()

def raw_msg(message, bot=bot):
	print(f"{message['u']}: {message['p']}")

bot.callback(raw_msg, cbid="__raw__") # If the cbid is not specifed, it will use the function name

```



