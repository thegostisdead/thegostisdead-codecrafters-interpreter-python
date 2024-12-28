import sys
from app.tokens import Token, TokenType
from app.scanner import Scanner
from app.parser import Parser, ParseError
from app.ast import AstPrinter
from app.interpreter import Interpreter
from app.exceptions import LoxRuntimeError
class Lox :
	had_error = False
	had_runtime_error = False
	interpreter: Interpreter = Interpreter()

	@staticmethod
	def run_file(filename: str, mode: str) :
		with open(filename, "rb") as file:
			file_bytes = file.read()
		raw_str = file_bytes.decode("utf-8")
		Lox.run(raw_str, mode)
		if Lox.had_error :
			exit(65)
		if Lox.had_runtime_error :
			exit(70)


	@staticmethod
	def run(source: str, mode: str):
		scanner = Scanner(source)
		tokens: list[Token] = scanner.scan_tokens()
		parser = Parser(tokens)

		try :
			statements = parser.parse()
			if mode == "tokenize" :
				for token in tokens:
					print(token)

			if mode == "parse" :
				if Lox.had_error:
					return
				print(AstPrinter().print(statements).lower())

			if mode == "evaluate":
				if Lox.had_error:
					return
				Lox.interpreter.evaluate(statements)

			if mode == "run":
				if Lox.had_error:
					return
				Lox.interpreter.interpret(statements)

		except ParseError as pe :
			Lox.error(pe.token, str(pe))

		except LoxRuntimeError as re :
			Lox.runtime_error(re)




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
		Lox.had_runtime_error = False

	@staticmethod
	def report(line: int, where: str, message: str):
		print(f"[line {line}] Error: {message}", file = sys.stderr)
		Lox.had_error = True

	@staticmethod
	def error(token: Token, message: str):

		if token.token_type == TokenType.EOF :
			Lox.report(token.line, " at end", message)
		else :
			Lox.report(token.line, " at '" + token.lexeme + "'", message)

	@staticmethod
	def runtime_error(error: LoxRuntimeError):
		print(str(error) +"\n[line " + str(error.token.line) + "]", file=sys.stderr)
		Lox.had_runtime_error = True