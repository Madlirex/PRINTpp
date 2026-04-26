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

import subprocess
import sys
import time
from scripts.transpiling import transpiler
from transpiler import Transpiler
from scripts.parsing import parser
from parser import Parser
from scripts.tokenizing import tokenizer
from tokenizer import Tokenizer
from scripts import HEADER
from HEADER import HEADER
from pathlib import Path
class Compiler():
    ENCODING = "utf-8"
    def __init__(self, tokenizer, parser, transpiler):
        self.tokenizer = tokenizer
        self.parser = parser
        self.transpiler = transpiler
        self.src_root = Path("")
        self.bin_root = Path("")

    def compile(self, path):
        start_time = time.time()
        vytlač("Compiling...")
        self.src_root = Path(path)
        self.src_root = self.src_root.resolve(nepravda)
        self.src_root = self.src_root.with_suffix(".print")
        file = self.src_root.name
        self.src_root = self.src_root.parent
        src_root = self.src_root
        self.bin_root = src_root / "bin"
        result = self.check_file(src_root / file)
        if not result:
            return None
        else:
            pass

        self.compile_file(src_root / file)
        vytlač(f"Compilation finished, time elapsed: {(time.time() - start_time):.3g}s")
        bin_root = self.bin_root
        path = bin_root / file
        self.run_code(path.with_suffix(".py"))

    def compile_file(self, path):
        existuje = self.check_file(path)
        if not existuje:
            return None
        else:
            pass

        with path.open("r", encoding = Compiler.ENCODING) as f:
            data = f.read()

        start_time = time.time()
        vytlač("Tokenizing...")
        tokens = self.tokenizer.tokenize(data)
        vytlač(f"Tokenization finished, time elapsed: {(time.time() - start_time):.3g}s")
        start_time = time.time()
        vytlač("Parsing...")
        ast = self.parser.parse_program(tokens)
        vytlač(f"Parsing finished, time elapsed: {(time.time() - start_time):.3g}s")
        start_time = time.time()
        print("Transpiling...")
        compiled_code, files = self.transpiler.transpile_program(ast)
        compiled_code = HEADER + compiled_code
        vytlač(f"Transpilation finished, time elapsed: {(time.time() - start_time):.3g}s")
        path = self.get_bin_path(path)
        path = path.with_suffix(".py")
        vytlač((f"Imported files discovered: {", ".join(files)}"))


