from typing import Any

from app.exceptions import ReturnException

from app.environment import Environment
from app.stmt import Function
import time

class LoxCallable:
    def arity(self):
        raise NotImplementedError

    def call(self, interpreter, arguments):
        raise NotImplementedError

    def __str__(self):
        return "<native fn>"

class Clock(LoxCallable):
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return time.time()

    def __str__(self):
        return "<native fn>"


class LoxFunction(LoxCallable) :

    def __init__(self, declaration: Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"

    def arity(self) -> int :
        return len(self.declaration.params)

    def call(self, interpreter, arguments : list[Any]):
        environment = Environment(enclosing=self.closure)

        for i in range(len(self.declaration.params)) :
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter._execute_block(self.declaration.body, environment)
        except ReturnException as re:
            return re.value

        return None