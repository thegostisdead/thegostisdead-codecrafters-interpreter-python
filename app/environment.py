from typing import Any, Optional
from app.tokens import Token
from app.exceptions import LoxRuntimeError

class Environment:
    def __init__(self,
                 enclosing: Optional[dict[str, Any]] = None
    ):
        self.enclosing = enclosing
        self.values : dict[str, Any] = dict()

    def define(self, name: str, value: Any):
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

    def __str__(self):
        return f"<Env defined_var={len(self.values.keys())} defined_vars=[{self.values.keys()}]>"