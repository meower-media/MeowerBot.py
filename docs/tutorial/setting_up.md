
<p align="center"><h1>Setting up MeowerBot.py </h1></p>

## Installing

Installing MeowerBot.py is as simple as using pip install!

```bash
pip install MeowerBot
```

## Your First Bot

MeowerBot.py is a simple library, with only a few chosen wrappers.

you start your bot with

```py
from MeowerBot import Bot

bot = Bot()
```

Now there are some important callbacks, and systems that make your life alot more easy

- 1. The command system

Example

```py

@bot.command(args=1, name="hello")
def command(ctx, name):
    ctx.send_msg(f"hello, {name}!")

```

- 2. The context system

The context system is MeowerBots way of abstracting raw websocket data, and commands from you.

it consists of 3 main parts.

   - 1. The CTX object
       The Ctx object initilises everything else to do with CTX, and contains all the methods to send messages by default

       it makes multi chat work by default
    
   - 2. the User object
       The user object stores all data the bot can get from a user, giving you the power to check whats there without having to set up a system to get that data, and then wait in your command

   - 3. the post object
       The Body of CTX. The message your bot is reacting to.


it is always activated everytime someone sends a post, that your bot receves

- 3. Callbacks

Callbacks are the meat and butter of your bot, allowing ultimate control over what data you have.

unforchently its to large to fit into this one markdown file. please go to [refrence](./refrence/callbacks/) to learn more

<p align="center" href="./cogs.md">
Next page
</p>