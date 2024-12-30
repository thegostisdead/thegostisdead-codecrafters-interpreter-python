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

    @abstractmethod
    def visit_variable_expr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visit_assign_expr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visit_logical_expr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visit_call_expr(self, expr: 'Expr'):
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


class Call(Expr) :
    def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]) -> None :
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_call_expr(self)

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

class Variable(Expr):

    def __init__(self, name: Token) -> None:
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_variable_expr(self)

class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_assign_expr(self)

class Logical(Expr):
    def __init__(self, left: Expr, operator : Token, right : Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_logical_expr(self)

