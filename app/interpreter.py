from app.expr import Visitor, Expr
from app.tokens import TokenType
from typing import Any

class Interpreter(Visitor):
    def _is_truthy(self, obj: Any) -> bool:
        if obj is None :
            return False
        if isinstance(obj, bool):
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
            return int(left) > int(right)

        if expr.operator.token_type == TokenType.GREATER_EQUAL:
            return int(left) >=  int(right)

        if expr.operator.token_type == TokenType.LESS:
            return int(left) < int(right)

        if expr.operator.token_type == TokenType.LESS_EQUAL:
            return int(left) <= int(right)

        if expr.operator.token_type == TokenType.MINUS :
            return int(left) - int(right)

        if expr.operator.token_type == TokenType.PLUS :
            if isinstance(left, int) and isinstance(right, int) :
                return int(left) + int(right)
            if isinstance(left, str) and isinstance(right, str) :
                return str(left) + str(right)
            return
        if expr.operator.token_type == TokenType.SLASH:
            return int(left) / int(right)

        if expr.operator.token_type ==TokenType.STAR :
            return int(left) * int(right)
        # Unreachable
        return None


    def visit_grouping_expr(self, expr: Expr):
        return self._evaluate(expr.expression)

    def visit_unary_expr(self, expr: Expr):
        right = self._evaluate(expr.right)
        if expr.operator.token_type == TokenType.BANG:
            return not self._is_truthy(right)
        if expr.operator.token_type == TokenType.MINUS:
            return - int(right)

        # Unreachable
        return None

    def _stringify(self, obj: Any):
        if obj is None :
            return "nil"
        if isinstance(obj, int):
            text = str(obj)
            if text.endswith(".0") :
                text = text[0:len(text) - 2]
            return text
        return str(obj)

    def interpret(self, expr: Expr):
        value = self._evaluate(expr)
        print(self._stringify(value).lower())