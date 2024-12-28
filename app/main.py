import sys
from app.lox import Lox

def main():

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command == "parse" :
        Lox.run_file(filename, mode="parse")

    elif command == "tokenize":
        Lox.run_file(filename, mode="tokenize")

    elif command == "evaluate":
        Lox.run_file(filename, mode="evaluate")

    elif command == "run":
        Lox.run_file(filename, mode="run")

    else :
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
