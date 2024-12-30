from typing import Any

from app.exceptions import ReturnException
from app.interpreter import LoxCallable, Interpreter
from app.environment import Environment
from app.stmt import Function


class LoxFunction(LoxCallable) :

    def __init__(self, declaration: Function):
        self.declaration = declaration

    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"

    def arity(self) -> int :
        return len(self.declaration.params)

    def call(self, interpreter: Interpreter, arguments : list[Any]):
        environment = Environment(interpreter.globals)
        for i in range(0, len(self.declaration.params)) :
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter._execute_block(self.declaration.body, environment)
        except ReturnException as re:
            return re.value

        return None