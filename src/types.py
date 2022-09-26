import typing
import weakref

if typing.TYPE_CHECKING:
    from .raw.bot import bot


class user:
    @classmethod
    async def from_api(cls, username, bot: "bot"):
        usr = await bot.api.get_user(username)
        return cls(
            username, bot, usr["uuid"], usr["pfp_data"], usr["quote"], usr["lvl"]
        )

    def __init__(self, name, bot: "bot", id, pfp, quote, lvl):

        self.name = name
        self._bot = bot
        self.id = id
        self.pfp = pfp
        self.quote = quote
        self.lvl = lvl
        self._ctx = None

    def add_ctx(self, ctx: "ctx"):
        self.ctx = weakref.ref(ctx)

    async def reply(self, msg):
        await self.ctx.send_msg(f"@{self.name} {msg}")


class message:
    @classmethod
    async def from_raw(cls, raw_data, bot: "bot"):
        if raw_data["u"] == "Discord":
            raw_data["u"] = raw_data["p"].split(":")[0]
            raw_data["p"] = raw_data["p"].split(":")[1].strip()

        return cls(
            raw_data["p"],
            await user.from_api(raw_data["u"], bot),
            msg["message_origin"],
            bot,
            raw_data,
        )

    def __init__(self, msg, user, origin, bot, raw):
        self.msg = msg
        self._ctx = None
        self._bot = bot
        self.origin = origin
        self.user = usr
        self.IsDiscord = raw["u"] == "Discord" and ":" in raw["p"]
        self.raw_data = raw


class ctx:
    def __init__(self, bot: "bot", raw_msg):
        self._bot = bot
        self.msg = message.from_raw(raw_msg, bot)
        self.user = msg.user
        self.IsDiscord = msg.IsDiscord

    async def send_msg(self, msg):
        await self._bot.send_msg(msg, self.msg.origin)


def make_ctx(bot, raw_msg):
    return ctx(bot, raw_msg)
