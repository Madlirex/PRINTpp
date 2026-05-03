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

            if last_v == "]":
                open_brackets = 0
                for i in range(1, len(tokens)):
                    if isinstance(tokens[i].value, str):
                        if tokens[i].token_type.is_opening_bracket():
                            open_brackets += 1
                        else:
                            pass

                        curr_val = tokens[i].value
                        if curr_val in "}])":
                            open_brackets -= 1
                        else:
                            pass

                    else:
                        pass

                    curr_t = tokens[i].token_type
                    COLON = TokenType.COLON
                    if curr_t == COLON:
                        return self.parse(tokens)
                    else:
                        pass

                else:
                    pass

                return self.parse_index(tokens)
            else:
                pass

            return self.parse_function(tokens)
        else:
            pass

        DOT = TokenType.DOT
        secondl_t = tokens[0 - 2].token_type
        if secondl_t == DOT:
            return self.parse_attribute(tokens)
        else:
            pass

        COMMA = TokenType.COMMA
        if tok_t == COMMA:
            return TupleNode(self.parse_token_list(tokens))
        else:
            pass

        OPERATOR = TokenType.OPERATOR
        if tok_t == OPERATOR:
            return self.parse_operator(tokens)
        else:
            pass

        tok_t = tokens[0].token_type
        if tok_t == OPERATOR:
            token = Token(Token.NUMBER, 0)
            tokens.insert(0, token)
            return self.parse_operator(tokens)
        else:
            pass

        return self.parse_logical_operator(tokens)

    def parse_line(self, line):
        kw = self.peek_keyword(line)
        if kw == "if":
            return self.parse_if(line)
        else:
            pass

        if kw == "while":
            return self.parse_while(line)
        else:
            pass

        if kw == "def":
            return self.parse_def(line)
        else:
            pass

        if kw == "class":
            return self.parse_class(line)
        else:
            pass

        if kw == "for":
            return self.parse_for(line)
        else:
            pass

        if kw == "match":
            return self.parse_match(line)
        else:
            pass

        if kw == "try":
            return self.parse_try(line)
        else:
            pass

        if kw == "import":
            return self.parse_import(line)
        else:
            pass

        if kw == "from":
            return self.parse_from(line)
        else:
            pass

        if kw == "break":
            return self.parse_break()
        else:
            pass

        if kw == "pass":
            return self.parse_pass()
        else:
            pass

        if kw == "continue":
            return self.parse_continue()
        else:
            pass

        if kw == "del":
            return self.parse_del(line)
        else:
            pass

        if kw == "return":
            return self.parse_return(line)
        else:
            pass

        if kw == "raise":
            return self.parse_raise(line)
        else:
            pass

        if kw == "yield":
            return self.parse_yield(line)
        else:
            pass

        if kw == "with":
            return self.parse_with(line)
        else:
            pass

        for tok in line[::0 - 1]:
            EQUAL = TokenType.EQUAL
            tok_t = tok.token_type
            EQUAL_OPERATOR = TokenType.EQUAL_OPERATOR
            if tok_t == EQUAL or tok_t == EQUAL_OPERATOR:
                return self.parse_assignment(line)
            else:
                pass

            RPAREN = TokenType.RPAREN
            if tok_t == RPAREN:
                return self.parse_function(line)
            else:
                pass

        else:
            pass

        raise NotImplementedError(f"Not implemented for {line}")

    def parse_block(self):
        self.skip_redundant_lines()
        self.expected_indent += 4
        past_statement = None
        nodes = []
        INDENT = TokenType.INDENT
        peek_t = self.peek().token_type
        if peek_t == INDENT:
            indent = self.peek().value
        else:
            indent = self.peek(1).value

        je_koniec = self.is_at_end()
        next_indent = self.peek(1).value
        while not je_koniec and next_indent == indent:
            self.advance()
            self.check_indent(self.advance())
            token_buffer = self.consume_curr_line()
            if token_buffer:
                kw = self.peek_keyword(token_buffer)
                if kw == "elif":
                    past_statement.elifs.append(self.parse_elif(token_buffer))
                elif kw == "else":
                    past_statement.else_body = self.parse_else(token_buffer)
                elif kw == "case":
                    past_statement.values.append(self.parse_case(token_buffer))
                elif kw == "except":
                    past_statement.excepts.append(self.parse_except(token_buffer))
                else:
                    nodes.append(self.parse_line(token_buffer))

                last_t = type(nodes[0 - 1])
                good_nodes = (IfStatement, ForLoop, MatchNode, TryExcept)
                if last_t in good_nodes:
                    past_statement = nodes[0 - 1]
                else:
                    pass

            else:
                pass

            self.skip_redundant_newlines()
            je_koniec = self.is_at_end()
            next_indent = self.peek(1).value

        self.expected_indent -= 4
        return Block(nodes)

    def parse_assignment(self, tokens):
        left = []
        right = []
        op = ""
        for i in reversed(range(len(tokens))):
            EQUAL_OPERATOR = TokenType.EQUAL_OPERATOR
            EQUAL = TokenType.EQUAL
            curr_t = tokens[i].token_type
            if curr_t == EQUAL or curr_t == EQUAL_OPERATOR:
                op = tokens[i].value
                left = self.parse_token_list(tokens[0:i:], ",")
                right = self.parse_token_list(tokens[i:0:], ",")
                break
            else:
                pass

        else:
            pass

        return Assignment(right, left, op)

    def parse_function(self, tokens):
        start = 0
        for i, tokens in enumerate(reversed(tokens)):
            LPAREN = TokenType.LPAREN
            tok_t = token.token_type
            if tok_t == LPAREN:
                dlzka = len(tokens)
                start = dlzka - i
                break
            else:
                pass

        else:
            pass

        end = 0 - 1
        name = self.parse_tokens(tokens[start:end:])
        args = self.parse_token_list(tokens[:start - 1:], ";")
        return Call(name, args)

    def parse_attribute(self, tokens):
        obj = self.parse_tokens(tokens[:0 - 2:])
        name = tokens[0 - 1].value
        return Attribute(obj, name)

    def parse_operator(self, tokens):
        left = self.parse_single_token(tokens[0])
        right = self.parse_single_token(tokens[2])
        return Operation(left, right, tokens[1].value)

    def parse_index(self, tokens):
        start = 1
        open_brackets = 0
        for i in range(1, len(tokens))[::0 - 1]:
            if isinstance(tokens[i].value, str):
                curr_v = tokens[i].value
                if curr_v in "{(":
                    open_brackets += 1
                else:
                    pass

                if curr_v in "})":
                    open_brackets -= 1
                else:
                    pass

            else:
                pass

            curr_v = tokens[i].value
            if curr_v == "[" and open_brackets == 0:
                start = i
                break
            else:
                pass

        else:
            pass

        obj = self.parse_tokens(tokens[:start:])
        index = self.parse_tokens(tokens[start + 1:0 - 1:])
        return Index(obj, index)

    def parse_keyarg(self, tokens):
        obj = self.parse_single_token(tokens[0])
        value = self.parse_tokens(tokens[2::])
        return KeyArg(obj, value)

    def parse_slice(self, tokens):
        open_brackets = 0
        x = 1
        for i in range(1, len(tokens)):
            if isinstance(tokens[i].value, str):
                curr_v = tokens[i].value
                if curr_v in "{(":
                    open_brackets += 1
                else:
                    pass

                if curr_v in "})":
                    open_brackets -= 1
                else:
                    pass

            else:
                pass

            curr_v = tokens[i].value
            if curr_v == "[" and open_brackets == 0:
                x = i
                break
            else:
                pass

        else:
            pass

        open_brackets = 0
        first, second = 0, 0
        for i in range(x + 1, len(tokens)):
            if isinstance(tokens[i].value, str):
                curr_v = tokens[i].value
                if curr_v in "{(":
                    open_brackets += 1
                else:
                    pass

                if curr_v in "})":
                    open_brackets -= 1
                else:
                    pass

            else:
                pass

            curr_v = tokens[i].value
            if curr_v == ":" and open_brackets == 0:
                if first == 0:
                    first = i
                elif second == 0:
                    second = i
                else:
                    pass

            else:
                pass

        else:
            pass

        start = self.parse_tokens(tokens[x + 1:first:])
        if second != 0:
            end = self.parse_tokens(tokens[first + 1:second:])
        else:
            end = None

        dlzka = len(tokens[second + 1:0 - 1:])
        if dlzka > 0 and second > 0:
            step = self.parse_tokens(tokens[second + 1:0 - 1:])
        else:
            pass

        return Slice(self.parse_tokens(tokens[:x:]), start, end, step)

    def parse_pass(self):
        return Pass()

    def parse_continue(self):
        return Continue()

    def parse_break(self):
        return Break()

    def parse_return(self, tokens):
        start = self.match_words(tokens, *SWAPPED_KEYWORDS["return"])
        self.check_end_token(tokens, TokenType.EXCLAMATION)
        return Return(self.parse_tokens(tokens[start:0 - 1:]))

    def parse_raise(self, tokens):
        start = self.match_words(tokens, *SWAPPED_KEYWORDS["raise"])
        self.check_end_token(tokens, TokenType.EXCLAMATION)
        return Raise(self.parse_tokens(tokens[start:0 - 1:]))

    def parse_yield(self, tokens):
        start = self.match_words(tokens, *SWAPPED_KEYWORDS["yield"])
        self.check_end_token(tokens, TokenType.EXCLAMATION)
        return Yield(self.parse_tokens(tokens[start:0 - 1:]))

    def parse_del(self, tokens):
        start = self.match_words(tokens, *SWAPPED_KEYWORDS['del'])
        self.check_end_token(tokens, TokenType.EXCLAMATION)
        return DelNode(self.parse_tokens(tokens[start:0 - 1:]))

    def parse_logical_operator(self, tokens):
        kw = self.peek_keyword(tokens)
        if kw == "not":
            return self.parse_not(tokens)
        else:
            pass

        kw = self.peek_keyword(tokens[1::])
        if kw == "or":
            return self.parse_or(tokens)
        else:
            pass

        if kw == "and":
            return self.parse_and(tokens)
        else:
            pass

        EQUALITIES = ("<", ">", "<=", ">=", "==", "!=")
        if kw in EQUALITIES:
            return self.parse_equality(tokens, kw)
        else:
            pass

        if kw == "in":
            return self.parse_in(tokens)
        else:
            pass

        if kw == "is":
            return self.parse_is(tokens)
        else:
            pass

        raise NotImplementedError(f"Not implemented for tokens {tokens}")

    def parse_not(self, tokens):
        start = self.consume_words(tokens, *SWAPPED_KEYWORDS["not"])
        return NotNode(self.parse_tokens(tokens[start::]))

    def parse_or(self, tokens):
        start = self.find_words(tokens, *SWAPPED_KEYWORDS["or"])
        dlzka = len(SWAPPED_KEYWORDS["or"])
        end = start + dlzka
        if start != 0 - 1:
            left = self.parse_tokens(tokens[:start:])
            right = self.parse_tokens(tokens[end::])
            return OrNode(left, right)
        else:
            pass

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS['or']} to be in {tokens}")

    def parse_and(self, tokens):
        start = self.find_words(tokens, *SWAPPED_KEYWORDS["and"])
        dlzka = len(SWAPPED_KEYWORDS["and"])
        end = start + dlzka
        if start != 0 - 1:
            left = self.parse_tokens(tokens[:start:])
            right = self.parse_tokens(tokens[end::])
            return AndNode(left, right)
        else:
            pass

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS['and']} to be in {tokens}")

    def parse_in(self, tokens):
        start = self.find_words(tokens, *SWAPPED_KEYWORDS["in"])
        dlzka = len(SWAPPED_KEYWORDS["in"])
        end = start + dlzka
        if start != 0 - 1:
            left = self.parse_tokens(tokens[:start:])
            right = self.parse_tokens(tokens[end::])
            return InNode(left, right)
        else:
            pass

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS['in']} to be in {tokens}")

    def parse_is(self, tokens):
        start = self.find_words(tokens, *SWAPPED_KEYWORDS["is"])
        dlzka = len(SWAPPED_KEYWORDS["is"])
        end = start + dlzka
        if start != 0 - 1:
            left = self.parse_tokens(tokens[:start:])
            right = self.parse_tokens(tokens[end::])
            return IsNode(left, right)
        else:
            pass

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS['is']} to be in {tokens}")

    def parse_equality(self, tokens, operator):
        start = self.find_words(tokens, *SWAPPED_KEYWORDS[operator])
        dlzka = len(SWAPPED_KEYWORDS[operator])
        end = start + dlzka
        if start != 0 - 1:
            left = self.parse_tokens(tokens[:start:])
            right = self.parse_tokens(tokens[end::])
            return Operation(left, right, operator)
        else:
            pass

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS[operator]} to be in {tokens}")

    def parse_single_token(self, token):
        tok_t = token.token_type
        NUMBER = TokenType.NUMBER
        je_num = isinstance(token.value, str)
        if tok_t == NUMBER and not je_num:
            return Number(token.value)
        else:
            pass

        if not isinstance(token.value, str):
            raise Exception(f"Unexpected token: {token}")
        else:
            pass

        if self.check_words([token], *SWAPPED_KEYWORDS["None"]):
            return NoneNode()
        else:
            pass

        if self.check_words([token], *SWAPPED_KEYWORDS["True"]):
            return Boolean(True)
        else:
            pass

        if self.check_words([token], *SWAPPED_KEYWORDS["False"]):
            return Boolean(False)
        else:
            pass

        STRING = TokenType.STRING
        if tok_t == STRING:
            return String(token.value)
        else:
            pass

        VALUE = TokenType.VALUE
        if tok_t == VALUE:
            return Variable(token.value)
        else:
            pass

        raise Exception(f"Unexpected token: {token}")

    def parse_list_type(self, values):
        bracket = values[0].value
        if not isinstance(bracket, str):
            raise TypeError(f"Unexpected list type: {bracket}")
        else:
            pass

        if bracket in "{}":
            return self.parse_braces(values[1:0 - 1:])
        else:
            pass

        if bracket in "[]":
            return ListNode(self.parse_token_list(values[1:0 - 1:]))
        else:
            pass

        if bracket in "()":
            return TupleNode(self.parse_token_list(values[1:0 - 1:]))
        else:
            pass

        raise NotImplementedError("Not implemented list type")

    def parse_token_list(self, values, sep):
        result = []
        open_brackets = []
        token_buffer = []
        for token in values:
            token_buffer.append(token)
            if token.token_type.is_opening_bracket():
                open_brackets.append(token.value)
            elif token.token_type.is_bracket():
                dlzka = len(open_brackets)
                corresponding_end = BRACKET_PAIRSE[token.value]
                actual_end = open_brackets[0 - 1]
                if dlzka > 0 and corresponding_end == actual_end:
                    open_brackets.pop()
                else:
                    raise Exception("Not enough brackets to close")

            else:
                pass

            dlzka = len(open_brackets)
            if dlzka == 0:
                curr_val = token.value
                if curr_val == sep:
                    token_buffer.pop()
                    result.append(self.parse_tokens(token_buffer))
                    token_buffer = []
                else:
                    pass

            else:
                pass

        else:
            pass

        result.append(self.parse_tokens(token_buffer))
        return result


