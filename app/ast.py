from app.tokens import Token, TokenType
from app.expr import ExprVisitor, Expr, Binary, Unary, Literal, Grouping, Variable, Logical, Call
class AstPrinter(ExprVisitor) :



  def print(self, expr: Expr) -> str :
    return expr.accept(self)

  def _parenthesize(self, name: str, *exprs: Expr):
    content = ' '.join(expr.accept(self) for expr in exprs)
    return f'({name} {content})'

  def visit_binary_expr(self, expr: Binary):
    return self._parenthesize(expr.operator.lexeme,
                        expr.left, expr.right)

  def visit_grouping_expr(self, expr: Grouping):
    return self._parenthesize("group", expr.expression)

  def visit_literal_expr(self, expr: Literal):
    if expr.value is None :
      return "nil"
    return str(expr.value)

  def visit_variable_expr(self, expr: Variable):
    return expr.name.lexeme

  def visit_assign_expr(self, expr: Variable):
    return self._parenthesize('=', expr.name.lexeme, expr.value)

  def visit_unary_expr(self, expr: Unary):
    return self._parenthesize(expr.operator.lexeme, expr.right)

  def visit_call_expr(self, expr: Call):
    return self._parenthesize('call', expr.callee, expr.arguments)

  def visit_logical_expr(self, expr: Logical):
    name = f'logical {expr.operator.lexeme}'
    return self._parenthesize(name, expr.left, expr.right)

if __name__ == "__main__" :
  expression = Binary(
    Unary(
      Token(TokenType.MINUS, "-", None, 1),
      Literal(123)),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(
      Literal(45.67)))

  print(AstPrinter().print(expression))
