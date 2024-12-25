from typing import LiteralString, Any
from enum import Enum

class TokenType(Enum):
	LEFT_PAREN = '('
	RIGHT_PAREN = ')'
	LEFT_BRACE = '{'
	RIGHT_BRACE = '}'
	COMMA = ','
	DOT = '.'
	MINUS = '-'
	PLUS = '+'
	SEMICOLON = ';'
	SLASH = '/'
	STAR = '*'

	# multiple char
	BANG = '!'
	BANG_EQUAL = '!='
	EQUAL = '='
	EQUAL_EQUAL = '=='
	GREATER = '>'
	GREATER_EQUAL = '>='
	LESS = '<'
	LESS_EQUAL = '=<'

	# Literals
	IDENTIFIER = 'IDENTIFIER'
	STRING = 'STRING'
	NUMBER = 'NUMBER'
	AND = 'and'
	CLASS = 'class'
	ELSE = 'else'
	FALSE = 'false'
	FUN = 'fun'
	FOR = 'for'
	IF = 'if'
	NIL = 'nil'
	OR = 'or'
	PRINT = 'print'
	RETURN = 'return'
	SUPER = 'super'
	THIS = 'this'
	TRUE = 'true'
	VAR = 'var'
	WHILE = 'while'

	EOF = 'EOF'


token_mapping_single_char = {
			'(': TokenType.LEFT_PAREN,
			')': TokenType.RIGHT_PAREN,
			'{': TokenType.LEFT_BRACE,
			'}': TokenType.RIGHT_BRACE,
			',': TokenType.COMMA,
			'.': TokenType.DOT,
			'-': TokenType.MINUS,
			'+': TokenType.PLUS,
			';': TokenType.SEMICOLON,
			'*': TokenType.STAR,
}


class Token:
	def __init__(self, token_type: TokenType, lexeme: str, literal, line: int):
		self.token_type = token_type
		self.lexeme = lexeme
		self.literal = literal
		self.line = line

	def __str__(self):
		# return f"<Token type={self.token_type} lexeme={self.lexeme} literal={self.literal} />"
		return f"{self.token_type.name} {self.lexeme} {self.literal}"


# https://craftinginterpreters.com/scanning.html#recognizing-lexemes

class Scanner:

	def __init__(self, source: str):
		self.source = source
		self.tokens: list[Token] = []
		self.start: int = 0
		self.current: int = 0
		self.line: int = 1

	def advance(self) -> str:
		char = self.source[self.current]
		self.current += 1
		return char

	def add_token(self, token_type: TokenType, literal: Any = None) -> None:
		text = self.source[self.start:self.current]
		self.tokens.append(Token(token_type, text, literal, self.line))


	def is_at_end(self) -> bool:
		return self.current >= len(self.source)

	def match(self, expected: str) -> bool:
		if self.is_at_end() :
			return False
		if self.source[self.current] != expected :
			return False

		self.current += 1
		return True
	def scan_token(self):
		c: str = self.advance()
		resolved_type = token_mapping_single_char.get(c, None)

		if resolved_type is None:
			# match for composed token
			if c == '!' :
				resolved_type = TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG
			elif c == '=':
				resolved_type = TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL
			elif c == '<':
				resolved_type = TokenType.LESS_EQUAL if self.match('=')  else TokenType.LESS
			elif c == '>':
				resolved_type = TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER
			else:
				raise ValueError(self.line, "Unexpected character.")

		self.add_token(resolved_type)

	def scan_tokens(self) -> list[Token]:
		while not self.is_at_end():
			self.start = self.current
			self.scan_token()

		self.tokens.append(Token(TokenType.EOF, "", None, self.line))
		return self.tokens