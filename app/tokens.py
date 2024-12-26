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

class Token:
	def __init__(self, token_type: TokenType, lexeme: str, literal, line: int):
		self.token_type = token_type
		self.lexeme = lexeme
		self.literal = literal
		self.line = line

	def __str__(self):
		return f"{self.token_type.name} {self.lexeme} {'null' if self.literal is None else self.literal}"

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

keywords: dict[str, TokenType] = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE
}