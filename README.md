# MeowerBot.py

A bot lib for Meower


## License

see [LICENSE](./LICENSE)


## docs

The Docs are located [here](./docs/callbacks.md)


## Quick Example

```py

from MeowerBot import Bot


bot = Bot(debug=False)


def handle_db_msg(message: Dict, bot:Bot=bot) -> None:
	if message['u'] == "Discord" and ": " in message['p']:
		message['u'] = message['p'].split(": ")[0]
		message['p'] = message['p'].split(": ")[1]

	if message['u'] == "Webhooks" and ": " in message['p']: # Webhooks should not be supported other then spliting the username off the post (so a webhooks user can still run things)
		message['p'] = message['p'].split(": ")  
		
bot.callback("post", handle_db_msg)

bot.start("username", "password")

```
