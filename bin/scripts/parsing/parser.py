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

    def consume_words(self, tokens, *words):
        if not self.match_words(tokens, *words):
            raise SyntaxError(f"Expected {' '.join(words)}, got {tokens}")
        else:
            pass

        return len(words)

    def find_words(self, tokens, *words):
        for i in range(len(tokens)):
            if self.match_words(tokens[i::], *words):
                return i
            else:
                pass

        else:
            pass

        return 0 - 1

    def peek_keyword(self, tokens):
        for words, replacement in KEYWORDS_LIST:
            if self.check_words(tokens, *words):
                return replacement
            else:
                pass

        else:
            pass

        return None

    def consume_keyword(self):
        for words, replacement in KEYWORDS_LIST:
            if self.check_words(*words):
                for _ in words:
                    self.advance()
                else:
                    pass

                return replacement
            else:
                pass

        else:
            pass

        return None

    def check_end_token(self, tokens, token_type):
        actual = tokens[0 - 1].token_type
        if actual != token_type:
            raise SyntaxError("Invalid syntax you illiterate swine")
        else:
            pass


    def check_indent(self, token):
        INDENT = TokenType.INDENT
        tok_t = token.token_type
        if tok_t == INDENT:
            value = token.value
            expected = self.expected_indent
            if not value == expected:
                raise IndentationError(f"Wrong indent {token.value}, expected {self.expected_indent}")
            else:
                pass

        else:
            pass


    def peek_curr_line(self):
        token_buffer = []
        i = 0
        NEWLINE = TokenType.NEWLINE
        COMMENT = TokenType.COMMENT
        tok_t = self.peek(i).token_type
        je_koniec = self.is_at_end()
        while not je_koniec and not tok_t == NEWLINE:
            token_buffer.append(self.peek(i))
            i += 1
            last_t = token_buffer[0 - 1].token_type
            if last_t == COMMENT:
                token_buffer.pop()
            else:
                pass

            je_koniec = self.is_at_end()
            tok_t = self.peek(i).token_type

        return token_buffer

    def consume_curr_line(self):
        token_buffer = []
        je_koniec = self.is_at_end()
        NEWLINE = TokenType.NEWLINE
        COMMENT = TokenType.COMMENT
        tok_t = self.peek().token_type
        while not je_koniec and not tok_t == NEWLINE:
            token_buffer.append(self.advance())
            last_t = token_buffer[0 - 1].token_type
            if last_t == COMMENT:
                token_buffer.pop()
            else:
                pass

            tok_t = self.peek().token_type
            je_koniec = self.is_at_end()

        return token_buffer

    def parse_program(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.expected_indent = 0 - 4
        program = Program(self.parse_block())
        return program

    def parse_tokens(self, tokens):
        dlzka = len(tokens)
        if dlzka == 1:
            return self.parse_single_token(tokens[0])
        else:
            pass

        if dlzka == 0:
            return None
        else:
            pass

        tok_t = tokens[1].token_type
        EQUAL = TokenType.EQUAL
        if tok_t == EQUAL:
            return self.parse_keyarg(tokens)
        else:
            pass

        if tokens[0 - 1].token_type.is_bracket():
            COMMA = TokenType.COMMA
            secondl_t = tokens[0 - 2].token_type
            last_v = tokens[0 - 1].value
            if secondl_t == COMMA or not last_v in "])":
                return self.parse_list_type(tokens)
            else:
                pass

        else:
            pass



