import builtins

RENAMES = {
    "vytlač": "print",
    "vtlač": "input",
    "dĺžka": "len",
    "rozsah": "range"
}

def _make_blocked(old_name, new_name):
    def blocked(*args, **kwargs):
        raise RuntimeError(f"Use '{new_name}' instead of '{old_name}'")
    return blocked

for new_name, old_name in RENAMES.items():
    original = getattr(builtins, old_name)

    globals()[new_name] = original

    globals()[old_name] = _make_blocked(old_name, new_name)

from enum import Enum, auto
class TokenType(Enum):
    VALUE = auto()
    EQUAL = auto()
    OPERATOR = auto()
    EQUAL_OPERATOR = auto()
    STRING = auto()
    NUMBER = auto()
    COMMENT = auto()
    QUESTION = auto()
    EXCLAMATION = auto()
    DOT = auto()
    COMMA = auto()
    COLON = auto()
    INDENT = auto()
    NEWLINE = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    EOF = auto()
    def is_bracket(self):
        BRACKETS = {TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACKET, TokenType.RBRACKET, TokenType.LBRACE, TokenType.RBRACE}
        result = self in BRACKETS
        return result

    def is_structural(self):
        STRUCTURALS = {TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACKET, TokenType.RBRACKET, TokenType.LBRACE, TokenType.RBRACE, TokenType.COMMA, TokenType.COLON, TokenType.NEWLINE, TokenType.INDENT}
        result = self in STRUCTURALS
        return result

    def is_opening_bracket(self):
        OPENING_BRACKETS = {TokenType.LBRACKET, TokenType.LBRACE, TokenType.LPAREN}
        result = self in OPENING_BRACKETS
        return result


class Token():
    def __init__(self, token_type, value = ""):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f"{self.token_type.name}: {self.values}"


