<p align="center">
<h1> \_\_raw\_\_ </h1>
</p>

the callback that gets triggered without editing the post at all. 

This acts the same as `on_msg in MeowerBot 1.x.x

## Arguments

### Bot

Required Keyword argument 

### post

The raw post object that is given by the Meower Server


## Example Code

```py
from MeowerBot import Bot

...

bot = Bot()
...

def raw_post(post, bot=bot):
   print(f"{post['u']}: {post['p']}")

bot.listener(raw_post, cbid="__raw__")
```
