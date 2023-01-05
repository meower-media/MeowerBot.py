# type: ignore # disable linter

from os import environ as env

from MeowerBot import Bot, __version__
from MeowerBot.API import MeowerAPI

bot = Bot(debug=True)
bot.api = None


def direct(val, listener, bot=bot):
    if listener == "__meowerbot__login":
        bot.api = MeowerAPI(val["payload"]["token"], val["payload"]["username"])
        bot.send_msg("Meower Stats: " + str(bot.api.statistics()))


bot.callback(direct, cbid="direct")

bot.run(env["uname"], env["password"])
