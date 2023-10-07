class BaseCustomException(Exception):
    def __init__(self, message=None) -> None:
        self.message = message
        super().__init__(self.message)
