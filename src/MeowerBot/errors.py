
class Error(Exception):
    pass

class MeowerError(Error):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CantConnectError(Error):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)