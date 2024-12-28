
class ASTCodeGen :

    def __init__(self):
        self.imports = ["from abc import ABC, abstractmethod", "from app.expr import Expr"]

    @staticmethod
    def generate_visitor(base_class: str, nodes : list[str]):
        header = [f"class {base_class}Visitor(ABC):\n", " \n"]
        methods = []
        for node in nodes :
            left, right = node.split(":")
            left = left.strip().lower()

            body = [
                "\t@abstractmethod\n",
                f"\tdef visit_{left}_{base_class.lower()}(self, expr: '{base_class}'):\n"
                f"\t\tpass\n"
            ]

            methods.append(''.join(body))


        return ''.join(header) + ''.join(methods)


    @staticmethod
    def generate_base_class(base_class: str) -> str:

        block = [
            f"class {base_class}(ABC):\n",
            "\t@abstractmethod\n",
            f"\tdef accept(self, visitor: {base_class}Visitor):\n"
            "\t\tpass\n"
        ]

        return ''.join(block)

    @staticmethod
    def generate_nodes(base_class: str, nodes: list[str]) -> str:
        classes = []
        for node in nodes :
            left, right = node.split(":")
            left = left.strip()

            block = [
                f"class {left}({base_class}):\n",
                "\tdef __init__(self, expression: Expr) -> None:\n",
                "\t\tself.expression = expression\n",
                f"\tdef accept(self, visitor: {base_class}Visitor) -> None:\n",
                f"\t\treturn visitor.visit_{left.lower()}_{base_class.lower()}(self)\n"
            ]

            classes.append(''.join(block))


        return ''.join(classes)

    def build_from_ast(self, base_class: str, nodes: list[str]):
        visitor = self.generate_visitor(base_class, nodes)
        base = self.generate_base_class(base_class)
        nodes = self.generate_nodes(base_class, nodes)
        for import_line in self.imports :
            print(import_line)
        print(visitor + "\n" + base + "\n" + nodes + "\n")


if __name__ == "__main__" :
    print(f"Run AST code gen...")

    code_generator = ASTCodeGen()
    code_generator.build_from_ast("Stmt", ["Expression : Expr expression", "Print: Expr expression"])
