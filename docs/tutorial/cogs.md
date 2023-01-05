<p align="center">
<h1>MeowerBot Cogs</h1>
</p>
MeowerBot cogs are basicly just commands that are in a class.

The name of the class is the name of the cog. 

you need diffrent imports for deeling with cogs

```py
# cog.py
from MeowerBot.cog import Cog
from MeowerBot.command import command
```

Next you create your cog class

```py
#cog.py
class YourCog(Cog):
    def __init__(self, bot):
        Cog.__init__(self)
        self.bot = bot
    
```

The commands are basicly the same for `bot.command`

you just use the imported `command` decorateor insted

```py
#cogs.py

class YourCog(Cog):
    def __init__(self, bot):
        Cog.__init__(self)
        self.bot = bot

    @command()
    def yourcommand(ctx):
        print("YourCommand Has Been RUN!")

        ctx.reply("hello!")

```

In your main file you need to import your `Cog` class

```py
#main.py
from MeowerBot import Bot
from cogs import YourCog

bot = Bot()

bot.register_cog(YourCog(bot))
```

