import sys
from typing import TextIO


def define_type(writer: TextIO, base_name: str, class_name: str, fields):
    pass

def define_ast(output_dir: str, base_name: str, types: list[str]):
    path = output_dir + "/" + base_name + ".py"
    with open(path, "w", encoding="utf-8") as writer:
        writer.write("\n")
        writer.write(f"abstract class {base_name} {{\n")
        writer.write("}\n")

        for type in types :
            class_name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            define_type(writer, base_name, class_name, fields)

def main():
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        sys.exit(64)

    output_dir = sys.argv[1]
    define_ast(output_dir, "Expr", [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Object value",
        "Unary    : Token operator, Expr right"]
    )


if __name__ == "__main__":
    main()