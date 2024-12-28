from app.tokens import Token

class ParseError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token

class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()