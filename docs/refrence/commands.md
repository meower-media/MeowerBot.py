<p align="center"><h1>Commands Refrence<h1></p>

this applys both to :meth: `MeowerBot.Bot.command`, and :func: `MeowerBot.command.command`

creating a command returns a :obj: `MeowerBot.command.AppCommand`. replacing your function

## args

	- name: str (or aname in bot.command, because breaking change i dont wanna make.)
		the name of the command
	
	- args: int
		the number of arguments the command takes

		if the command takes infinite arguments use 0.


# Subcommands

A subcommand is a command that basicly takes the first argument as the command name, and the rest as the arguments. 

This makes it easy to make a command that has multiple subcommands. And have subcommands that have subcommands as they are the same as normal commands, but are handled by the parent command.

## args
	- name: str
		the name of the command
	
	- args: int
		the number of arguments the command takes

		if the command takes infinite arguments use 0.


## example

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
