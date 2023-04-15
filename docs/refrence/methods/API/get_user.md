# MeowerAPI.get_user

This method gets a user from the api. However it does not convert the user to a User object (Because the user object calls this method).

It is best to create an instance of the user class instead of using this method.

## args

- username: str
  The username of the user you want to get

## example

```py

from MeowerBot import Bot
from MeowerBot.context import User

bot = Bot()
bot.user = User("YourUsername")


def login(bot=bot):
	user = bot.get_user(bot.user.username)
	print(user)


bot.callback(login, cbid="login") # when cbid is not specified it defaults to the function name (in this case "login")

```