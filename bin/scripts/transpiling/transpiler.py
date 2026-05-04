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

    def visit_assignment(self, node):
        return f"{self.transpile_nodes(node.left)} {node.operator} {self.transpile_nodes(node.right)}"

    def visit_attribute(self, node):
        return f"{self.transpile(node.obj)}.{node.name}"

    def visit_call(self, node):
        if isinstance(node.func, String):
            quotes = node.func.value[0 - 1]
            prefix = ""
            first = node.func.value[0]
            if first != quotes:
                prefix = first
            else:
                pass

            return f"{node.func.value[len(prefix)+1:-1]}({prefix}{quotes}{self.transpile_nodes(node.args)}{quotes})"
        else:
            pass

        name = self.transpile(node.func)
        if name in RENAMES:
            name = RENAMES[name]
        elif name in INVALID_RENAMES:
            raise RuntimeError(f"Use '{INVALID_RENAMES[name]}' instead of '{name}'")
        else:
            pass

        return f"{name}({self.transpile_nodes(node.args)})"

    def visit_index(self, node):
        return f"{self.transpile(node.obj)}[{self.transpile(node.index)}]"

    def visit_slice(self, node):
        start, end, step = "", "", ""
        if node.start:
            start = self.transpile(node.start)
        else:
            pass

        if node.end:
            end = self.transpile(node.end)
        else:
            pass

        if node.step:
            step = self.transpile(node.step)
        else:
            pass

        return f"{self.transpile(node.obj)}[{start}:{end}:{step}]"

    def visit_pass(self):
        return "pass"

    def visit_continue(self):
        return "continue"

    def visit_break(self):
        return "break"

    def visit_return(self, node):
        return f"return {self.transpile(node.value)}"

    def visit_yield(self, node):
        return f"yield {self.transpile(node.value)}"

    def visit_raise(self, node):
        return f"raise {self.transpile(node.value)}"

    def visit_del(self, node):
        return f"del {self.transpile(node.value)}"

    def visit_in(self, node):
        return f"{self.transpile(node.left)} in {self.transpile(node.right)}"

    def visit_is(self, node):
        return f"{self.transpile(node.left)} is {self.transpile(node.right)}"

    def visit_or(self, node):
        return f"{self.transpile(node.left)} or {self.transpile(node.right)}"

    def visit_and(self, node):
        return f"{self.transpile(node.left)} and {self.transpile(node.right)}"

    def visit_not(self, node):
        return f"not {self.transpile(node.value)}"

    def visit_operation(self, node):
        return f"{self.transpile(node.left)} {node.operator} {self.transpile(node.right)}"


