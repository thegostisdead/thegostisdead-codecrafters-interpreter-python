from typing import Any
from app.tokens import Token
from app.exceptions import LoxRuntimeError
class Environment:

    def __init__(self, environment=None):
        if environment is None:
            environment = {}
        self.values : dict[str, Any] = environment

    def define(self, name: str, value: str):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def assign(self, name: Token, value : Any):
        if name.lexeme in self.values :
            self.values[name.lexeme] = value
            return
        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")