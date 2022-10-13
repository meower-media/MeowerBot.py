# skipcq
class BotError(Exception):
    pass


# skipcq
class LoginError(BotError):
    pass


# skipcq
class ConnectionError(BotError):
    pass


# skipcq
class PostError(BotError):
    pass
