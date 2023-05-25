# type: ignore # disable linter

from logging import DEBUG, basicConfig
from os import environ as env

from MeowerBot import Bot, __version__
from MeowerBot.API import MeowerAPI

basicConfig(level=DEBUG)

bot = Bot()
bot.api = None


def direct(val, listener, bot=bot):
    if listener == "__meowerbot__login":
        bot.send_msg("Meower Stats: " + str(bot.api.statistics()))


bot.callback(direct, cbid="direct")

bot.run(env["uname"], env["password"])
