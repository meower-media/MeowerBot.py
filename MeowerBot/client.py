from .Bot import Bot


class Client(Bot):
    def __init__(self, debug=False, debug_out=sys.__stdout__) -> None:
        super().__init__(self, prefix=None, debug=debug, debug_out=debug_out)
        delattr(self, "command")
        delattr(self, "register_cog")
        
