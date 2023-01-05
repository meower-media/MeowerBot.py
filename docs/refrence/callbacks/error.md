<p align="center">
<h1> # Error Callback </h1>
</p>
This callback gets called when an exception gets raised.

## args

### error

The error that caused this callback to get called

### bot

A required keyword argument

## example

```py
import traceback
from MeowerBot import Bot

...

bot = Bot()

...

def error(e, bot=bot):
   traceback.print_exc(e)

bot.callback(error)
```
