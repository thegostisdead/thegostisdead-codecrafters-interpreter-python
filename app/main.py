import sys
from app.lox import Interpreter

def main():

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command == "parse" :
        Interpreter.run_file(filename)

    elif command == "tokenize":
        Interpreter.run_file(filename)

    else :
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)



if __name__ == "__main__":
    main()
