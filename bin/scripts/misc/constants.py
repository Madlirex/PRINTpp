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

def keyword_length(keyword):
    return dĺžka(keyword)

KEYWORDS = {("čo", "ak"): "if", ("ibaže"): "elif", ("inak"): "else", ("kým", "platí", "že"): "while", ("pre", "každé"): "for", ("trieda"): "class", ("definuje"): "def", ("skús"): "try", ("okrem"): "except", ("na", "koniec"): "finally", ("v"): "in", ("sa", "rovná"): "==", ("je", "menšie", "ako"): "<", ("je", "väčšie", "ako"): ">", ("je", "menšie", "alebo", "rovné", "ako"): "<=", ("je", "väčšie", "alebo", "rovné", "ako"): ">=", ("sa", "nerovná"): "!=", ("neplatí"): "not", ("alebo"): "or", ("a"): "and", ("je"): "is", ("definuj"): "def", ("zmaž"): "del", ("vráť"): "return", ("výnos"): "yield", ("ako"): "as", ("importuj"): "import", ("z"): "from", ("zlom"): "break", ("pokračuj"): "pass", ("preskoč"): "continue", ("klamstvo"): "False", ("pravda"): "True", ("nič"): "None", ("verejné"): "global", ("nelokálna"): "nonlocal", ("využi"): "with", ("porovnaj"): "match", ("v", "prípade", "že"): "case", ("vyvráť"): "raise", ("skrátená", "funkcia,", "väčšinou", "anonymná", "a", "bez", "mena,", "používa", "sa", "pri", "krátkych", "operáciach", "alebo", "vo", "vnútri", "funkcií", "ako", "argument"): "lambda"}
SWAPPED_KEYWORDS = dict()
for key, value in KEYWORDS.items():
    SWAPPED_KEYWORDS[key] = value
else:
    pass

KEYWORDS_LIST = sorted(KEYWORDS.items(), key = keyword_length, reverse = True)
BRACKETS = {"(": TokenType.LPAREN, ")": TokenType.RPAREN, "[": TokenType.LBRACKET, "]": TokenType.RBRACKET, "{": TokenType.LBRACE, "}": TokenType.RBRACE}
BRACKET_PAIRS = {")": "(", "]": "[", "}": "{"}
OPERATORS = {'+', '-', '*', '**', '/', '%', '//', '==', '!=', '<', '<=', '>', '>=', '&', '|', '^', '~', '<<', '>>'}
