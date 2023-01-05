from os import environ as env

from MeowerBot import Bot, __version__

bot: Bot = Bot(debug=True, prefix="/")


@bot.command()
def test(ctx, *args):
    ctx.send_msg(" ".join(args) + "\n mb.py " + __version__)


bot.run(env["username"], env["password"])
