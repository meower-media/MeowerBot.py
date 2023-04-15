<p align="center"><h1>Commands Reference<h1></p>

This applies to both :meth: `MeowerBot.Bot.command` and :func: `MeowerBot.command.command`

Creating a command returns a :obj: `MeowerBot.command.AppCommand`, replacing your function

# Arguments

	- name: str (or aname in bot.command, because there is a breaking change I do not want to make.)
		the name of the command
	
	- args: int
		the number of arguments the command takes

		if the command takes infinite arguments use 0.


# Subcommands

A subcommand is a command that takes the first argument as the command name and the rest as arguments. 

This makes it easy to make a command that has multiple subcommands. And have subcommands that have subcommands as they are the same as normal commands, but are handled by the parent command.

## Arguments
	- name: str
		the name of the command
	
	- args: int
		the number of arguments the command takes

		if the command takes infinite arguments use 0.


## Example Code

```py

from MeowerBot import Bot

bot = Bot()

@bot.command()
def test(ctx):
	ctx.send("test")

@test.subcommand()
def sub(ctx):
	ctx.send("sub")

```
