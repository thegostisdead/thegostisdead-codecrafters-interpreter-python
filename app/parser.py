from app.tokens import Token, TokenType

from app.expr import Expr, Grouping, Literal, Binary, Unary
from app.stmt import Stmt, Print, Expression
from app.exceptions import ParseError, LoxRuntimeError

class Parser :
    def __init__(self, tokens: list[Token]):
        self._tokens : list[Token] = tokens
        self._current : int = 0

    def parse(self) -> list[Stmt]:
        statements : list[Stmt] = []
        while not self._is_at_end() :
            statements.append(self._statement())
        return statements

    @staticmethod
    def error(token: Token, message: str):
        return ParseError(token, message)

    def _peek(self) -> Token :
        return self._tokens[self._current]
    def _is_at_end(self) -> bool :
        return self._peek().token_type == TokenType.EOF

    def _previous(self) :
        return self._tokens[self._current - 1]
    def _advance(self) :
        if not self._is_at_end() :
            self._current += 1
        return self._previous()

    def _check(self, token_type : TokenType) -> bool :
        if self._is_at_end() :
            return False
        return self._peek().token_type == token_type

    def _consume(self, token_type: TokenType, message: str):
        if self._check(token_type):
            return self._advance()
        raise self.error(self._peek(), message)

    def _consume_and_runtime_crash(self, token_type: TokenType, message: str):
        if self._check(token_type):
            return self._advance()
        raise LoxRuntimeError(self._peek(), message)

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal(False)
        elif self._match(TokenType.TRUE):
            return Literal(True)
        elif self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN) :
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self._peek(), "Expect expression.")
    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS) :
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        return self._primary()

    def _factor(self) -> Expr :
        expr = self._unary()
        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)
        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)
        return expr
    def _comparison(self) -> Expr :
        expr = self._term()
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL) :
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)
        return expr
    def _equality(self) -> Expr:
        expr = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL) :
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _expression(self) -> Expr:
        return self._equality()

    def _print_statement(self):
        value = self._expression()
        self._consume_and_runtime_crash(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def _expression_statement(self):
        expr = self._expression()
        self._consume_and_runtime_crash(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)
    def _statement(self) -> Stmt:
        if self._match(TokenType.PRINT) : return self._print_statement()
        return self._expression_statement()

    def _match(self, *types : TokenType) -> bool:
        for token_type in types:
            if self._check(token_type) :
                self._advance()
                return True
        return False

    def _synchronize(self):
        self._advance()
        while not self._is_at_end() :
            if self._previous().token_type == TokenType.SEMICOLON:
                return

            if self._peek().token_type in (
                    TokenType.CLASS,
                    TokenType.VAR,
                    TokenType.FOR,
                    TokenType.IF,
                    TokenType.WHILE,
                    TokenType.PRINT,
                    TokenType.RETURN,
            ):
                return
            self._advance()
