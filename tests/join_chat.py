from MeowerBot import Bot, __version__
from os import environ as env
bot = Bot(prefix="/")
import time
from logging import basicConfig, DEBUG

basicConfig(level=DEBUG)

exited = False

def login_callback(bot=bot):
    print("Logged in")

    bot.enter_chat("livechat")


bot.callback(login_callback, cbid="login")

bot.run(env['username'], env['password'])