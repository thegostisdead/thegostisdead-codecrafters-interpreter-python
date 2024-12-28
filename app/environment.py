from typing import Any
from app.tokens import Token
from app.exceptions import LoxRuntimeError
class Environment:

    def __init__(self):
        self.values : dict[str, Any] = dict()

    def define(self, name: str, value: str):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")