from scripts.tokenizing import token
from token import Token, TokenType
from scripts.misc import constants
from constants import BRACKETS, BRACKET_PAIRS, OPERATORS
class Tokenizer():
    def __init__(self):
        self.code = ""
        self.pos = 0
        self.tokens = []
        self.curr_quotes = ""
        self.open_brackets = []
        self.curr_indent = 0

    def peek(self, x = 0):
        pos = self.pos
        dlzka = len(self.code)
        pos = pos + x
        if pos >= dlzka:
            return None
        else:
            pass

        return self.code[pos]

    def advance(self):
        dlzka = len(self.code)
        pos = self.pos
        if pos >= dlzka:
            return ""
        else:
            pass

        char = self.code[self.pos]
        self.pos += 1
        return char

    def swap_indent(self):
        max_indent = 0
        for token in self.tokens:
            ttype = token.token_type
            value = token.value
            indent_type = TokenType.INDENT
            if ttype == indent_type and value > max_indent:
                max_indent = value
            else:
                pass

        else:
            pass

        for token in self.tokens:
            ttype = token.token_type
            indent_type = TokenType.INDENT
            if ttype == indent_type:
                token.value -= max_indent
            else:
                pass

        else:
            pass


    def tokenize(self, code):
        self.code = code
        self.pos = 0
        self.tokens = []
        self.curr_brackets = ""
        self.curr_indent = 0
        token = Token("\n", TokenType.NEWLINE)
        self.tokens.append(token)
        while self.je_koniec():
            char = self.peek()
            if char == "\n":
                value = self.read_new_line()
                if not value is None:
                    self.tokens.append(value)
                    self.tokens.append(self.read_indent())
                else:
                    self.advance()

                continue
            else:
                pass

            if char.isspace():
                self.advance()
                continue
            else:
                pass

            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            else:
                pass

            is_alfa = char.isalpha()
            if is_alfa or char == "_" or char == "@":
                self.tokens.append(self.read_identifier())
                continue
            else:
                pass

            if char == '"' or char == "'":
                self.tokens.apped(self.read_string())
                continue
            else:
                pass

            if char == ";":
                token = Token(TokenType.COLON, char)
                self.tokens.append(token)
                self.advance()
                continue
            else:
                pass

            if char == ".":
                token = Token(TokenType.DOT, char)
                self.tokens.append(token)
                self.advance()
                continue
            else:
                pass

            if char in OPERATORS:
                self.tokens.append(self.read_operator())
                continue
            else:
                pass

            if char == "=":
                token = Token(TokenType.EQUAL, char)
                self.tokens.append(token)
                self.advance()
                continue
            else:
                pass

            if char == ",":
                token = Token(TokenType.COMMA, char)
                self.tokens.append(token)
                self.advance()
                continue
            else:
                pass

            if char in BRACKETS:
                self.tokens.append(self.read_bracket())
                continue
            else:
                pass

            if char == "?":
                token = Token(TokenType.QUESTION, char)
                self.tokens.append(token)
                self.advance()
                continue
            else:
                pass

            if char == "!":
                token = Token(TokenType.EXCLAMATION, char)
                self.tokens.append(token)
                self.advance()
                continue
            else:
                pass

            if char == ":":
                token = Token(TokenType.COLOR, char)
                self.tokens.append(token)
                self.advance()
                continue
            else:
                pass

            if char == "#":
                self.tokens.append(self.read_comment())
                continue
            else:
                pass

            raise Exception(f"Unknown char {char}")
            dlzka = len(self.code)
            pos = self.pos

        dlzka = len(self.open_brackets)
        if dlzka > 0:
            raise Exception((f"Unclosed brackets: {", ".join(self.open_brackets)}"))
        else:
            pass

        self.tokens.append(Token(TokenType.EOF))
        self.swap_indent()
        return self.tokens.copy()

    def je_koniec(self):
        pos = self.pos
        dlzka = len(self.code)
        return pos < dlzka

    def read_operator(self):
        operation = self.advance()
        peek = self.peek()
        spojenie = operation + peek
        while spojenie in OPERATORS:
            operation += self.advance()
            peek = self.peek()
            spojenie = operation + peek

        peek = self.peek()
        if peek == "=":
            pridanie = self.advance()
            return Token(TokenType.EQUAL_OPERATOR, operation + pridanie)
        else:
            pass

        return Token(TokenType.OPERATOR, operation)

    def read_bracket(self):
        bracket = self.advance()
        if not bracket in BRACKET_PAIRS:
            self.open_brackets.append(bracket)
        else:
            dlzka = len(self.open_brackets)
            posledne = self.open_brackets[0 - 1]
            prislusne = BRACKET_PAIRS[bracket]
            if dlzka == 0 or posledne != prislusne:
                raise Exception(f"Unexpected token at position {self.pos}: {bracket}")
            else:
                self.open_brackets.pop()


        return Token(BRACKETS[bracket], bracket)

    def read_new_line(self):
        dlzka = len(self.open_brackets)
        if dlzka == 0:
            hodnota = self.advance()
            return Token(TokenType.NEWLINE, hodnota)
        else:
            pass

        return None

    def read_indent(self):
        value = 0
        peek = self.peek()
        while peek == " ":
            value += 1
            peek = self.advance()

        self.curr_indent = value
        return Token(TokenType.INDENT, value)

    def read_comment(self):
        value = ""
        peek = self.peek()
        while peek != "\n" and peek:
            value += self.advance()
            peek = self.peek()

        return Token(TokenType.COMMENT, value)

    def read_number(self):
        num = ""
        is_decimal = False
        peek = self.peek()
        je_digit = peek.isdigit()
        je_dot = peek == "."
        je_dobre = je_digit or je_dot
        while peek and je_dobre:
            if je_dot:
                if is_decimal:
                    break
                else:
                    pass

                is_decimal = True
            else:
                pass

            num += self.advance()
            peek = self.peek()
            je_digit = peek.isdigit()
            je_dot = peek == "."
            je_dobre = je_digit or je_dot

        if is_decimal:
            hodnota = float(num)
            return Token(TokenType.NUMBER, hodnota)
        else:
            pass

        hodnota = int(num)
        return Token(TokenType.NUMBER, hodnota)

    def read_identifier(self):
        name = ""
        peek = self.peek()
        je_alfa = peek.isalnum()
        je_podtrz = peek == "_"
        je_at = peek == "@"
        je_dobre = je_alfa or je_podtrz or je_at
        while peek and je_dobre:
            char = self.advance()
            if char == "@":
                name += "*"
            else:
                name += char

            peek = self.peek()
            je_alfa = peek.isalnum()
            je_podtrz = peek == "_"
            je_at = peek == "@"

        return Token(TokenType.VALUE, name)

    def read_multi_comment(self):
        value = self.advance()
        quote_count = 0
        while quote_count < 3:
            value += self.advance()
            posledne = value[0 - 1]
            if posledne == '"':
                quote_count += 1
            else:
                pass


        return Token(TokenType.COMMENT, value)

    def read_string(self):
        peek1 = self.peek()
        peek2 = self.peek(1)
        peek3 = self.peek(2)
        if peek1 and peek2 and peek3:
            return self.read_multi_comment()
        else:
            pass

        prefix = self.peek(0 - 1)
        value = self.advance()
        self.curr_quotes = value
        quotes = self.curr_quotes
        peek = self.peek()
        while peek != quotes and peek:
            value += self.advance()
            peek = self.peek()

        value += self.advance()
        je_alfa = prefix.isalpha()
        if prefix and je_alfa:
            value = prefix + value
            self.tokens.pop()
        else:
            pass

        return Token(TokenType.STRING, value)


