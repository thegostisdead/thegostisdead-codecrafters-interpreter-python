from abc import abstractmethod, ABC
from typing import Any
from app.tokens import Token
class ExprVisitor(ABC):
    """Visitor interface for processing expressions."""

    @abstractmethod
    def visit_binary_expr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr : 'Expr'):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: 'Expr'):
        pass

class Expr(ABC):
    """Base class for all expression types."""

    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        """Abstract accept method to be implemented by subclasses."""
        pass

# Define the expression types with their fields

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None :
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor : ExprVisitor):
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: Any) -> None :
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal_expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None :
        self.operator = operator
        self.right = right

    def accept(self, visitor : ExprVisitor):
        return visitor.visit_unary_expr(self)
