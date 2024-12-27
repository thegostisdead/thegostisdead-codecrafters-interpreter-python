from app.expr import Visitor, Expr
from app.tokens import TokenType, Token
from app.exceptions import LoxRuntimeError
from typing import Any

class Interpreter(Visitor):
    def _is_truthy(self, obj: Any) -> bool:
        if obj is None :
            return False
        if type(obj) == type(True):
            return bool(obj)
        return True

    def _is_equal(self, a : Any, b : Any):
        if a is None and b is None:
            return True
        if a is None :
            return False

        return a == b
    def _evaluate(self, expr: Expr):
        return expr.accept(self)

    def _check_number_operand(self, operator: Token,  operand: Any):
        if isinstance(operand, float) : return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(self, operator: Token, left: Any, right: Any):
        if  isinstance(left, float) and isinstance(right, float) : return
        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def visit_literal_expr(self, expr: Expr):
        return expr.value

    def visit_binary_expr(self, expr: Expr):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)


        if expr.operator.token_type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)

        if expr.operator.token_type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)

        if expr.operator.token_type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return float(left) > float(right)

        if expr.operator.token_type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) >=  float(right)

        if expr.operator.token_type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) < float(right)

        if expr.operator.token_type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        if expr.operator.token_type == TokenType.MINUS :
            self._check_number_operands(expr.operator, left, right)
            return float(left) - float(right)

        if expr.operator.token_type == TokenType.PLUS :
            if isinstance(left, float) and isinstance(right, float) :
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str) :
                return str(left) + str(right)
            raise LoxRuntimeError(expr.operator,"Operands must be two numbers or two strings.")

        if expr.operator.token_type == TokenType.SLASH:
            return float(left) / float(right)

        if expr.operator.token_type ==TokenType.STAR :
            self._check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        # Unreachable
        return None


    def visit_grouping_expr(self, expr: Expr):
        return self._evaluate(expr.expression)

    def visit_unary_expr(self, expr: Expr):
        right = self._evaluate(expr.right)
        if expr.operator.token_type == TokenType.BANG:
            return not self._is_truthy(right)
        if expr.operator.token_type == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return - float(right)

        # Unreachable
        return None

    def _stringify(self, obj: Any):
        if obj is None :
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0") :
                text = text[0:len(text) - 2]
            return text
        return str(obj)

    def interpret(self, expr: Expr):
        try :
           value = self._evaluate(expr)
           print(self._stringify(value).lower())
        except LoxRuntimeError as re :
            from app.lox import Lox
            Lox.runtime_error(re)