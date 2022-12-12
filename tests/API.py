
from MeowerBot import Bot, __version__
from MeowerBot.API import MeowerAPI

from os import environ as env


bot = Bot(debug=True)
bot.api = None

def direct(val, listener):
    if listener == "__meowerbot__login":
        bot.api = MeowerAPI(val['payload']['token'], val['payload']['username']) 
        bot.send_msg("Stats: " + bot.api.statistics())

   

bot.callback(direct, cbid="direct")

bot.run(env['username'], env['password'])
