from app.scanner import Scanner, Token

class Interpreter :
	def __init__(self):
		pass

	def run_file(self, filename: str) :
		with open(filename, "rb") as file:
			file_bytes = file.read()
		raw_str = file_bytes.decode("utf-8")
		self.run(raw_str)

	def run(self, source: str):
		scanner = Scanner(source)
		tokens : list[Token] = scanner.scan_tokens()
		exit(65) if scanner.error else exit(0)
