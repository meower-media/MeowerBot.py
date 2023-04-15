# Bot.register_cog

Adds a cog to a bot.

## args

- cog: MeowerBot.Cog

## example

```py

from MeowerBot import Bot
from cog import MyCog

bot = Bot()

bot.register_cog(MyCog())

```


# Bot.deregister_cog

Removes a cog from a bot.

## args

- cog: str
	The name of the cog you want to remove

## example

```py

from MeowerBot import Bot
from cog import MyCog

bot = Bot()

bot.register_cog(MyCog())

bot.deregister_cog("MyCog")

```
