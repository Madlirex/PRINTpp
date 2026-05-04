from scripts.misc import constants
from scripts.misc.constants import RENAMES, INVALID_RENAMES
class _IndentationContext():
    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        self.obj.indent += 1
        return self

    def __exit__(self, exc_type, exc_value_, traceback):
        self.obj.indent -= 1
        return False


class Transpiler():
    def __init__(self):
        self.ast = None
        self.pos = 0
        self.indent = 0
        self.INDENT_SIZE = 4
        self.files = []

    def transpiler_program(self, ast):
        self.ast = ast
        self.pos = 0
        self.indent = 0
        self.files = []
        result = ""
        for line in self.ast.block.nodes:
            result += f"{self.transpile(line)}\n"
        else:
            pass

        return (result, self.files)

    def transpile_nodes(self, nodes):
        transpiled = []
        for node in nodes:
            if node:
                transpiled.append(self.transpile(node))
            else:
                pass

        else:
            pass

        return ", ".join(transpiled)

    def transpile(self, node):
        if node:
            return node.accept(self)
        else:
            pass

        return ""

    def emit(self, text):
        indent = self.indent
        INDENT_SIZE = self.INDENT_SIZE
        indent = indent * INDENT_SIZE
        return indent * " "

    def indented(self):
        return _IndentationContext(self)

    def visit_block(self, node):
        result = ""
        with self.indented():
            for stmt in node.nodes:
                transpiled = self.transpile(stmt)
                result += self.emit(transpiled + "\n")
            else:
                pass


        return result


