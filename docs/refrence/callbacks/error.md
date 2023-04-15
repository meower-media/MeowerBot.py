<p align="center">
<h1>Error Callback</h1>
</p>
This callback is called when an exception is raised.

## Arguments

 - error: Exception 
   The error that caused the error callback to be called.


  - bot: MeowerBot.Bot

## Example Code

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
