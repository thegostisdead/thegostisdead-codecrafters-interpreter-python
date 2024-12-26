import sys
from app.tokens import Token, TokenType
from app.scanner import Scanner
from app.parser import Parser, ParseError
from app.ast import AstPrinter
from app.interpreter import Interpreter
class Lox :
	had_error = False
	interpreter: Interpreter = Interpreter()

	@staticmethod
	def run_file(filename: str, mode: str) :
		with open(filename, "rb") as file:
			file_bytes = file.read()
		raw_str = file_bytes.decode("utf-8")

		Lox.run(raw_str, mode)

		if Lox.had_error :
			exit(65)


	@staticmethod
	def run(source: str, mode: str):
		try :
			scanner = Scanner(source)
			if mode == "tokenize" :
				tokens: list[Token] = scanner.scan_tokens()
				for token in tokens:
					print(token)

			if mode == "parse" :
				tokens: list[Token] = scanner.scan_tokens()
				parser = Parser(tokens)
				expression = parser.parse()
				if Lox.had_error:
					return
				print(AstPrinter().print(expression).lower())

			if mode == "evaluate":
				tokens: list[Token] = scanner.scan_tokens()
				parser = Parser(tokens)
				expression = parser.parse()
				Lox.interpreter.interpret(expression)


		except ParseError as pe :
			Lox.error(pe.token, str(pe))


	@staticmethod
	def run_prompt():
		while True:
			try:
				line = input("> ")
				if line is None or line.strip() == "":
					break
				Lox.run(line)
			except EOFError:
				break
		Lox.had_error = False

	@staticmethod
	def report(line: int, where: str, message: str):
		#print("[line " + str(line) + "] Error " + where + ": " + message, file=sys.stderr)
		print(f"[line {line}] Error: {message}", file = sys.stderr)
		Lox.had_error = True

	@staticmethod
	def error(token: Token, message: str):

		if token.token_type == TokenType.EOF :
			Lox.report(token.line, " at end", message)
		else :
			Lox.report(token.line, " at '" + token.lexeme + "'", message)
