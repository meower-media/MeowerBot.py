# MeowerAPI.get_user_posts

This method gets the posts of a user. It does not conver the posts to a post object, it just returns the raw request json.


## args

- username: str
  The username of the user you want to get the posts of

- page: int
  The page you want to get

  If not specified it defaults to 1


## example

```py

from MeowerBot import Bot


bot = Bot()

def login(bot=bot):
	user = bot.get_user_posts("YourUsername")
	print(user)

bot.callback(login, cbid="login") # when cbid is not specified it defaults to the function name (in this case "login")

```