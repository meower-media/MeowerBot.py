from os import environ as env

from MeowerBot import Bot, __version__

bot = Bot(prefix="/")
import time
from logging import DEBUG, basicConfig

basicConfig(level=DEBUG)

exited = False


def login_callback(bot=bot):
    print("Logged in")

    while True:
        bot.send_typing()

        time.sleep(1)

        if exited:
            break


def exit_callback(bot=bot):
    global exited
    exited = True


bot.callback(login_callback, cbid="login")
bot.callback(exit_callback, cbid="close")

bot.run(env["username"], env["password"])
