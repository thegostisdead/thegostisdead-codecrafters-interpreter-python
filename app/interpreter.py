from typing import Any
from app.tokens import TokenType, Token
from app.exceptions import LoxRuntimeError, ReturnException
from app.expr import ExprVisitor, Expr, Variable, Logical, Call
from app.stmt import Stmt, StmtVisitor, Expression, Print, Var, Block, If, \
    While, Function, Return
from app.environment import Environment
from app.functions import LoxFunction, Clock, LoxCallable



class Interpreter(ExprVisitor, StmtVisitor):


    def __init__(self):
        self.globals = Environment()
        self.globals.define("clock", Clock())
        self.environment = self.globals

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def execute(self, stmt: Stmt):
        if stmt is None :
            exit(65)
        stmt.accept(self)

    def interpret(self, statements: list[Stmt]):
        for statement in statements:
            self.execute(statement)

    def _is_truthy(self, obj: Any) -> bool:
        if obj is None:
            return False

        if isinstance(obj, bool):
            return obj

        return True

    def _is_equal(self, a : Any, b : Any):
        return a == b

    @staticmethod
    def _is_number(obj: Any) -> bool:
        return isinstance(obj, (int, float)) and not isinstance(obj, bool)

    def _check_number_operand(self, operator: Token,  operand: Any):
        if self._is_number(operand) : return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(self, operator: Token, left: Any, right: Any):
        if self._is_number(left) and self._is_number(right) : return
        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def visit_literal_expr(self, expr: Expr):
        return expr.value

    def visit_function_stmt(self, stmt: Function):
        func = LoxFunction(stmt)
        self.environment.define(stmt.name.lexeme, func)
        return None

    def visit_binary_expr(self, expr: Expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)


        if expr.operator.token_type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)

        if expr.operator.token_type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)

        if expr.operator.token_type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return left > right

        if expr.operator.token_type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return left >= right

        if expr.operator.token_type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return left < right

        if expr.operator.token_type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return left <= right

        if expr.operator.token_type == TokenType.MINUS :
            self._check_number_operands(expr.operator, left, right)
            return left - right

        if expr.operator.token_type == TokenType.PLUS :
            if self._is_number(left) and self._is_number(right) :
                return left + right

            # for string concat
            if isinstance(left, str) and isinstance(right, str) :
                return left + right

            raise LoxRuntimeError(expr.operator,"Operands must be two numbers or two strings.")

        if expr.operator.token_type == TokenType.SLASH:
            self._check_number_operands(expr.operator, left, right)
            return left / right

        if expr.operator.token_type == TokenType.STAR :
            self._check_number_operands(expr.operator, left, right)
            return left * right

        return None

    def visit_expression_stmt(self, stmt: Expression):
        self.evaluate(stmt.expression)
        return None

    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self._stringify(value))
        return None

    def visit_logical_expr(self, expr: Logical):
        left = self.evaluate(expr.left)

        if expr.operator.token_type == TokenType.OR :
            if self._is_truthy(left):
                return left
        else :
            if not self._is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_return_stmt(self, stmt: Return):
        value = None
        if stmt.value is not None :
            value = self.evaluate(stmt.value)

        raise ReturnException(value)

    def visit_var_stmt(self, stmt: Var):
        value = None
        if stmt.initializer is not None :
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_call_expr(self, expr: Call):
        callee = self.evaluate(expr.callee)
        arguments = []
        for arg in expr.arguments :
            arguments.append(self.evaluate(arg))

        if not isinstance(callee, LoxCallable) :
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        function = callee

        if len(arguments) != function.arity() :
            raise LoxRuntimeError(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
        return function.call(self, arguments)

    def visit_block_stmt(self, stmt: Block):
        self._execute_block(stmt.statements, Environment(enclosing=self.environment))
        return None

    def visit_variable_expr(self, expr: Variable):
        return self.environment.get(expr.name)

    def visit_grouping_expr(self, expr: Expr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Expr):
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenType.BANG:
            return not self._is_truthy(right)
        if expr.operator.token_type == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return - right

        return None

    def visit_assign_expr(self, expr: 'Expr'):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_while_stmt(self, stmt: While):
        while self._is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

        return None

    def visit_if_stmt(self, stmt: If):
        if self._is_truthy(self.evaluate(stmt.condition)) :
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None :
            self.execute(stmt.else_branch)

    def _execute_block(self, statements: list[Stmt], environment: Environment):
        previous = self.environment
        try :
            self.environment = environment
            for statement in statements :
                self.execute(statement)
        finally:
           self.environment = previous

    def _stringify(self, obj: Any):
        if obj is None:
            return "nil"

        if isinstance(obj, bool):
            return str(obj).lower() # True -> true

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[0:len(text) - 2]
            return text
        return str(obj)

