# type: ignore # disable linter

from MeowerBot import Bot, __version__
from MeowerBot.API import MeowerAPI

from os import environ as env

from logging import basicConfig, DEBUG

basicConfig(level=DEBUG)

bot = Bot()
bot.api = None 
def direct(val, listener, bot=bot):
    if listener == "__meowerbot__login":
        bot.api = MeowerAPI(val['payload']['token'], val['payload']['username']) 
        bot.send_msg("Meower Stats: " + str(bot.api.statistics()))
   

bot.callback(direct, cbid="direct")

bot.run(env['uname'], env['password'])
