from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.transpiling import itranspiler
    from itranspiler import ITranspiler
else:
    pass

class Node():
    def accept(self, visitor):
        raise NotImplementedError


class Block(Node):
    def __init__(self, nodes = None):
        self.nodes = nodes
        if nodes is None:
            self.nodes = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_block(self)


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable(self)


class Number(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_number(self)


class String(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_string(self)


class Attribute(Node):
    def __init__(self, obj, name):
        self.obj = obj
        self.name = name

    def accept(self, visitor):
        return visitor.visit_attribute(self)


class Call(Node):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def accept(self, visitor):
        return visitor.visit_call(self)


class Assignment(Node):
    def __init__(self, left, right, operator = "="):
        self.left = left
        self.right = right
        self.operator = operator

    def accept(self, visitor):
        return visitor.visit_assignment(self)


class IfStatement(Node):
    def __init__(self, condition, body, elifs = None, else_body = None):
        self.condition = condition
        self.body = body
        self.elifs = elifs
        self.else_body = else_body
        if elifs is None:
            self.elifs = []
        else:
            pass

        if else_body is None:
            self.else_body = Block([Pass()])
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_if(self)


class Return(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return(self)


class FunctionDef(Node):
    def __init__(self, name, body, params = None):
        self.name = name
        self.params = params
        self.body = body
        if params is None:
            self.params = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_function(self)


class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while(self)


class TryExcept(Node):
    def __init__(self, body, excepts = None):
        self.body = body
        self.excepts = excepts
        if excepts is None:
            self.excepts = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_try(self)


class Lambda(Node):
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_lambda(self)


class ForLoop(Node):
    def __init__(self, variable, expression, body, else_body = None):
        self.variable = variable
        self.body = body
        self.expression = expression
        self.else_body = else_body
        if else_body is None:
            self.else_body = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_for(self)


class ClassDef(Node):
    def __init__(self, name, body, parents = None):
        self.name = name
        self.body = body
        self.parents = parents
        if parents is None:
            self.parents = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_class(self)


class TernaryOp(Node):
    def __init__(self, condition, value1, value2):
        self.condition = condition
        self.value1 = value1
        self.value2 = value2

    def accept(self, visitor):
        return visitor.visit_ternary(self)


class ListComprehension(Node):
    def __init__(self, variable, expression, body = None, filter_condition = None):
        self.body = body
        self.variable = variable
        self.expression = expression
        self.filter = filter_condition
        if body is None:
            self.body = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_list_comp(self)


class ListNode(Node):
    def __init__(self, values = None):
        self.values = values
        if values is None:
            self.values = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_list(self)


class TupleNode(Node):
    def __init__(self, values = None):
        self.values = values
        if values is None:
            self.values = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_tuple(self)


class SetNode(Node):
    def __init__(self, values = None):
        self.values = values
        if values is None:
            self.values = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_set(self)


class DictionaryNode(Node):
    def __init__(self, keys = None, values = None):
        self.keys = keys
        self.values = values
        if keys is None:
            self.keys = []
        else:
            pass

        if values is None:
            self.values = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_dict(self)


class Boolean(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_bool(self)


class NoneNode(Node):
    def accept(self, visitor):
        return visitor.visit_none(self)


class Index(Node):
    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

    def accept(self, visitor):
        return visitor.visit_index(self)


class Slice(Node):
    def __init__(self, obj, start = None, end = None, step = None):
        self.obj = obj
        self.start = start
        self.end = end
        self.step = step

    def accept(self, visitor):
        return visitor.visit_slice(self)


class Import(Node):
    def __init__(self, modules, aliases = None):
        self.modules = modules
        self.aliases = aliases
        if aliases is None:
            self.aliases = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_import(self)


class FromImport(Node):
    def __init__(self, path, modules, aliases = None):
        self.path = path
        self.modules = modules
        self.aliases = aliases
        if aliases is None:
            self.aliases = []
        else:
            pass


    def accept(self, visitor):
        return visitor.visit_from_import(self)


class Raise(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_raise(self)


class Break(Node):
    def accept(self, visitor):
        return visitor.visit_break(self)


class Continue(Node):
    def accept(self, visitor):
        return visitor.visit_continue(self)


class Pass(Node):
    def accept(self, visitor):
        return visitor.visit_pass(self)


class Yield(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_yield(self)


class MatchNode(Node):
    def __init__(self, variable, values):
        self.variable = variable
        self.values = values

    def accept(self, visitor):
        return visitor.visit_match(self)


class AndNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_and(self)


class OrNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_or(self)


class NotNode(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_not(self)


class Operation(Node):
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

    def accept(self, visitor):
        return visitor.visit_operation(self)


class InNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_in(self)


class IsNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_is(self)


class KeyArg(Node):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def accept(self, visitor):
        return visitor.visit_keyarg(self)


class Program(Node):
    def __init__(self, block = None):
        dlzka = len(block.nodes)
        if not block or dlzka == 0:
            self.block = Block([Pass()])
        else:
            self.block = block



class DelNode(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_del(self)


class WithNode(Node):
    def __init__(self, statement, body, alias = None):
        self.statement = statement
        self.body = body
        self.alias = alias

    def accept(self, visitor):
        return visitor.visit_with(self)


