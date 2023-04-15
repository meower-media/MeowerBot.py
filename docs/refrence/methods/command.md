# command

This method is used to create a command in a cog.

## args

- name: str
  The name of the command

- args: int

	The number of arguments the command takes
 
    If the command takes infinite arguments use 0.


## example

```py

from MeowerBot.cog import Cog

class MyCog(Cog):

	def __init__(self, bot):
		self.bot = bot

	@command("test")
	def test(self, ctx):
		ctx.send("test")

```


# command.subcommand

This method is used to create a subcommand in a cog.

## args

- name: str
  The name of the command

- args: int

	The number of arguments the command takes
 
	If the command takes infinite arguments use 0.


## example

```py

from MeowerBot.cog import Cog

class MyCog(Cog):

	def __init__(self, bot):
		self.bot = bot

	@command("test")
	def test(self, ctx):
		ctx.send("test")

	@test.subcommand("sub")
	def sub(self, ctx):
		ctx.send("sub")

```
