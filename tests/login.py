

from MeowerBot import Bot, __version__
from os import environ as env


bot = Bot(debug=True)

def login(bot=bot):
	bot.send_msg("TESTING!!!!!!!! O_O")
	bot.send_msg("MeowerBot.py " + __version__)


def msg(msg, **_):
	if msg['p'].endswith("#test"): bot.send_msg("TEEEEEST", to="livechat")

bot.callback("login", login)
bot.run(env['username'], env['password'])


