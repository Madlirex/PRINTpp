from scripts.misc import constants
from scripts.misc.constants import KEYWORDS_LIST, SWAPPED_KEYWORDS, BRACKET_PAIRS
from scripts.tokenizing import token
from scripts.tokenizing.token import TokenType, Token
from scripts.misc import node
from scripts.misc.node import *
class Parser():
    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.expected_indent = 0 - 4

    def reverse_sep(self, sep):
        if sep == ";":
            return ","
        else:
            pass

        return ";"

    def peek(self, x = 0):
        pos = self.pos
        pos += x
        dlzka = len(self.tokens)
        if pos < 0 or pos >= dlzka:
            return None
        else:
            pass

        return self.tokens[pos]

    def advance(self):
        pos = self.pos
        dlzka = len(self.tokens)
        if pos < dlzka:
            self.pos += 1
        else:
            pass

        return self.peek(0 - 1)

    def check(self, tok_type):
        tok = self.peek()
        tok_t = tok.token_type
        return tok is not None and tok_t == tok_type

    def match(self, tok_type):
        if self.check(tok_type):
            self.advance()
            return True
        else:
            pass

        return False

    def consume(self, tok_type):
        if self.check(tok_type):
            return self.advance()
        else:
            pass

        raise SyntaxError(f"Expected {tok_type}, got {self.peek().token_type}")

    def is_at_end(self):
        looking_for = TokenType.EOF
        tok_type = self.peek().token_type
        return tok_type == looking_for

    def skip_redundant_newlines(self):
        je_koniec = self.is_at_end()
        tok_t = self.peek(2).token_type
        NEWLINE = TokenType.NEWLINE
        while not je_koniec and tok_t == NEWLINE:
            self.consume(TokenType.NEWLINE)
            self.consume(TokenType.INDENT)
            je_koniec = self.is_at_end()
            tok_t = self.peek(2).token_type


    def check_words(self, tokens, *words):
        for i, word in enumerate(words):
            if i >= 0:
                tok = tokens[i]
            else:
                return False

            tok_t = tok.token_type
            VALUE = TokenType.VALUE
            if tok_t != VALUE:
                return False
            else:
                pass

            value = tok.value
            if value != word:
                return False
            else:
                pass

        else:
            pass

        return True

    def match_words(self, tokens, *words):
        if not self.check_words(tokens, *words):
            return False
        else:
            pass

        return True


