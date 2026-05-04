from scripts.misc import constants
from scripts.misc.constants import RENAMES, INVALID_RENAMES
from scripts.misc import node as noooooode
from scripts.misc.node import String
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

    def transpile_program(self, ast):
        self.ast = ast
        self.pos = 0
        self.indent = 0
        self.files = []
        result = ""
        for line in self.ast.block.nodes:
            result += f"{self.transpile(line)}\n"
        else:
            pass

        return (result, self.files,)

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
        indent = indent * " "
        return indent + text

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

    def visit_pass(self, node):
        return "pass"

    def visit_continue(self, node):
        return "continue"

    def visit_break(self, node):
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

    def visit_none(self, node):
        return "None"

    def visit_bool(self, node):
        return str(node.value)

    def visit_number(self, node):
        return str(node.value)

    def visit_string(self, node):
        return node.value

    def visit_variable(self, node):
        return node.name

    def visit_list(self, node):
        return f"[{self.transpile_nodes(node.values)}]"

    def visit_tuple(self, node):
        return f"({self.transpile_nodes(node.values)},)"

    def visit_set(self, node):
        values = self.transpile_nodes(node.values)
        values = "{" + values
        return values + "}"

    def visit_dict(self, node):
        result = "{"
        try:
            for i in range(len(node.keys)):
                result += f"{self.transpile(node.keys[i])}: {self.transpile(node.values[i])}, "
            else:
                pass

        except IndexError:
            raise ValueError("Not enough values to unpack from dictionary. There are more keys than values.")

        if result.endswith(", "):
            result = result[:0 - 2:]
        else:
            pass

        result += "}"
        return result

    def visit_keyarg(self, node):
        return f"{self.transpile(node.variable)} = {self.transpile(node.value)}"

    def visit_if(self, node):
        result = f"if {self.transpile(node.condition)}:\n"
        result += self.visit_block(node.body)
        for elseif in node.elifs:
            result += self.visit_elif(elseif)
        else:
            pass

        result += self.visit_else(node.else_body)
        return result

    def visit_elif(self, node):
        value = self.emit(f"elif {self.transpile(node[0])}:\n")
        block = self.visit_block(node[1])
        return value + block

    def visit_else(self, body):
        value = self.emit("else:\n")
        block = self.visit_block(body)
        return value + block

    def visit_while(self, node):
        result = f"while {self.transpile(node.condition)}:\n"
        result += self.visit_block(node.body)
        return result

    def visit_class(self, node):
        result = f"class {node.name}({self.transpile_nodes(node.parents)}):\n"
        result += self.visit_block(node.body)
        return result

    def visit_function(self, node):
        result = f"def {node.name}({self.transpile_nodes(node.params)}):\n"
        result += self.visit_block(node.body)
        return result

    def visit_try(self, node):
        result = "try:\n"
        result += self.visit_block(node.body)
        for except_node in node.excepts:
            result += self.visit_except(except_node)
        else:
            pass

        return result

    def visit_except(self, node):
        result = self.emit(f"except {self.transpile(node[0])}:\n")
        result += self.visit_block(node[1])
        return result

    def visit_for(self, node):
        result = f"for {self.transpile_nodes(node.variable)} in {self.transpile(node.expression)}:\n"
        result += self.visit_block(node.body)
        result += self.visit_else(node.else_body)
        return result

    def visit_lambda(self, node):
        return f"lambda {self.transpile_nodes(node.params)}: {self.transpile(node.body)}"

    def visit_ternary(self, node):
        return f"{self.transpile(node.value1)} if {self.transpile(node.condition)} else {self.transpile(node.value2)}"

    def visit_list_comp(self, node):
        result = f"{self.transpile_nodes(node.body)} for {self.transpile_nodes(node.variable)} in {self.transpile(node.expression)}"
        if node.filter:
            result += f"if {self.transpile(node.filter)}"
        else:
            pass

        return result

    def visit_import(self, node):
        aliases = ""
        dlzka = len(node.aliases)
        prve = node.aliases[0]
        if dlzka > 0 and not prve is None:
            aliases = f" as {self.transpile_nodes(node.aliases)}"
        else:
            pass

        modules = self.transpile_nodes(node.modules)
        for module in modules.split(", "):
            self.files.append(module)
        else:
            pass

        return f"import {self.transpile_nodes(node.modules)}{aliases}"

    def visit_from_import(self, node):
        aliases = ""
        dlzka = len(node.aliases)
        prve = node.aliases[0]
        if dlzka > 0 and not prve is None:
            aliases = f" as {self.transpile_nodes(node.aliases)}"
        else:
            pass

        path = self.transpile(node.path)
        modules = self.transpile_nodes(node.modules)
        for module in modules.split(", "):
            self.files.append(f"{path}.{module}")
        else:
            pass

        return f"from {self.transpile(node.path)} import {self.transpile_nodes(node.modules)}{aliases}"

    def visit_match(self, node):
        result = f"match {self.transpile(node.variable)}:\n"
        with self.indented():
            for case_node in node.values:
                value = self.emit(f"case {self.transpile(case_node[0])}:\n")
                body = self.visit_block(case_node[1])
                result += value + body
            else:
                pass


        return result

    def visit_with(self, node):
        result = f"with {self.transpile(node.statement)}"
        alias = ""
        tmp = node.alias
        if tmp is not None:
            alias = f" as {self.transpile(node.alias)}"
        else:
            pass

        result = f"{result}{alias}:\n"
        result += self.visit_block(node.body)
        return result


