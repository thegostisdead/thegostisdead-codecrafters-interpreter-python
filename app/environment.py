from typing import Any
from app.tokens import Token
class Environment:

    def __init__(self):
        self.values : dict[str, Any] = dict()

    def define(self, name: str, value: str):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        raise RuntimeError(name, "Undefined variable '" + name.lexeme + "'.")