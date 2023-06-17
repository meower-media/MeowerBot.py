
<p align="center"><h1>Setting up MeowerBot.py </h1></p>

## Installing

Installing MeowerBot.py is as simple as using pip install!

```bash
pip install MeowerBot
```

## Your First Bot

MeowerBot.py is a simple library, with only a few chosen wrappers.

You should start off your bot with

```py
from MeowerBot import Bot

bot = Bot()
```

There are some important callbacks, and systems that make developing a bot much easier.

- 1. The command system

Example

```py

@bot.command(args=0, name="hello")
def command(ctx):
    ctx.send_msg(f"hello")

```

There are also subcommands.

```py

@command.subcommand(name="world")
def subcommand(ctx, name):
    ctx.send_msg(f"hello, world!")

```

- 2. The context system

The context system is MeowerBot.py's way of processing raw websocket data and commands from you. It consists of 3 main parts.

   - 1. The CTX object
       The CTX object initilises everything else to do with CTX, and contains all the methods to send messages by default. It makes multiple chats work by default.
    
   - 2. The user object
       The user object stores all data the bot can get from a user, giving you the power to check what is there without having to set up a system to get that data, and then wait in your command

   - 3. The post object
       The Body of CTX, which is also the message your bot is replying to.


It is always activated everytime someone sends a post, that your bot receves

[Next](./callbacks.md)