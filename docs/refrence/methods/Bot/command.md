# Bot.command

A decorator that creates a command, and automatically adds it to the bot.

## args

- aname: str 
  The name of the command

- args: int
	  The number of arguments the command takes

  		If the command takes infinite arguments use 0.

## example

```py

from MeowerBot import Bot

bot = Bot()

@bot.command()
def test(ctx):
	ctx.send("test")

```

