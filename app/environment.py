from typing import Any
from app.tokens import Token
from app.exceptions import LoxRuntimeError
class Environment:
    def __init__(self, environment=None, enclosing=None):
        if environment is None:
            environment = {}
        if enclosing is None :
            self.enclosing = None
        else :
            self.enclosing : Environment = enclosing
        self.values : dict[str, Any] = environment

    def define(self, name: str, value: Any):
        # print(f"Defining variable: {name} with value: {value}")
        if not isinstance(self.values, dict):
            self.values = {}
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)

        if self.enclosing is not None :
            return self.enclosing.get(name)
        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def assign(self, name: Token, value : Any):
        if name.lexeme in self.values :
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None :
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")