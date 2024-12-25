from typing import Any
from enum import Enum
import sys
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
		return f"{self.token_type.name} {self.lexeme} {'null' if self.literal is None else self.literal}"


# https://craftinginterpreters.com/scanning.html#recognizing-lexemes

class Scanner:

	def __init__(self, source: str):
		self.source = source
		self.tokens: list[Token] = []
		self.start: int = 0
		self.current: int = 0
		self.line: int = 1
		self.error = False

	def advance(self) -> str:
		char = self.source[self.current]
		self.current += 1
		return char

	def add_token(self, token_type: TokenType, literal: Any = None) -> None:
		text = self.source[self.start:self.current]
		self.tokens.append(Token(token_type, text, literal, self.line))

	def is_digit(self, char: str):
		return char.isdigit()

	def peek_next(self):
		if self.current + 1 >= len(self.source):
			return '\0'
		return self.source[self.current + 1]

	def number(self):
		while self.is_digit(self.peek()):
			self.advance()

		if self.peek() == '.' and self.is_digit(self.peek_next()):
			self.advance()

			while self.is_digit(self.peek()) :
				self.advance()
		self.add_token(TokenType.NUMBER, float(self.source[self.start: self.current]))
	def is_at_end(self) -> bool:
		return self.current >= len(self.source)

	def peek(self) -> str:
		if self.is_at_end() :
			return '\0'
		return self.source[self.current]

	def match(self, expected: str) -> bool:
		if self.is_at_end() :
			return False
		if self.source[self.current] != expected :
			return False

		self.current += 1
		return True

	def string(self):
		while self.peek() != '"' and not self.is_at_end():
			if self.peek() == '\n' :
				self.line += 1
			self.advance()
		if self.is_at_end() :
			self.error = True
			print(f"[line {self.line}] Error: Unterminated string.", file=sys.stderr)
			return
		self.advance()
		value = str(self.source[self.start + 1: self.current - 1])
		self.add_token(TokenType.STRING, value)

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
			elif c == '/' :

				if self.match('/') :
					# A comment goes until the end of the line.
					while self.peek() != '\n' and not self.is_at_end() :
						self.advance()
				else :
					self.add_token(TokenType.SLASH)
				return
			elif c in [' ', '\r', '\t'] :
				# Ignore whitespace.
				return
			elif c == '\n' :
				self.line += 1
				return
			elif c == '"':
				self.string()
				return
			else:

				if self.is_digit(c) :
					self.number()
				print(f"[line {self.line}] Error: Unexpected character: {c}", file=sys.stderr)
				self.error = True
				return
				#raise ValueError(self.line, "Unexpected character.")
		self.add_token(resolved_type)

	def scan_tokens(self) -> list[Token]:
		while not self.is_at_end():
			self.start = self.current
			self.scan_token()

		token = Token(TokenType.EOF, "", None, self.line)
		self.tokens.append(token)
		return self.tokens
