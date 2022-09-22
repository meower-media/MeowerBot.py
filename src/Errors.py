class BotError(Exception):
    pass


class LoginError(BotError):
    pass


class ConnectionError(BotError):
    pass


class PostError(BotError):
    pass
