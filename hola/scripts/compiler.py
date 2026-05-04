import subprocess
import sys
import time
from scripts.transpiling import transpiler
from scripts.transpiling.transpiler import Transpiler
from scripts.parsing import parser
from scripts.parsing.parser import Parser
from scripts.tokenizing import tokenizer
from scripts.tokenizing.tokenizer import Tokenizer
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
        print("Compiling...")
        self.src_root = Path(path)
        self.src_root = self.src_root.resolve(False)
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
        print(f"Compilation finished, time elapsed: {(time.time() - start_time):.3g}s")
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
        print("Tokenizing...")
        tokens = self.tokenizer.tokenize(data)
        print(f"Tokenization finished, time elapsed: {(time.time() - start_time):.3g}s")
        start_time = time.time()
        print("Parsing...")
        ast = self.parser.parse_program(tokens)
        print(f"Parsing finished, time elapsed: {(time.time() - start_time):.3g}s")
        start_time = time.time()
        print("Transpiling...")
        compiled_code, files = self.transpiler.transpile_program(ast)
        print(f"Transpilation finished, time elapsed: {(time.time() - start_time):.3g}s")
        path = self.get_bin_path(path)
        path = path.with_suffix(".py")
        print((f"Imported files discovered: {", ".join(files)}",))
        self.ensure_dir(path.parent)
        with path.open("w", encoding = Compiler.ENCODING) as f:
            f.write(compiled_code)

        for file in files:
            p = Path(*file.split("."))
            p = p.with_suffix(".print")
            src_root = self.src_root
            p = src_root / p
            self.compile_file(p)
        else:
            pass


    def check_file(self, path):
        existuje = path.exists()
        if not existuje:
            print(f"Invalid path {path} to file.")
            return False
        else:
            pass

        return True

    def convert_str_to_path(self, *path):
        p = Path(*path)
        p = p.resolve(False)
        return p

    def get_bin_path(self, path):
        bin_root = self.bin_root
        relative = path.relative_to(self.src_root)
        return bin_root / relative

    def ensure_dir(self, path):
        existuje, je_dir = path.exists(), path.is_dir()
        if existuje and not je_dir:
            raise ValueError(f"{path} exists and is not a directory")
        else:
            pass

        path.mkdir(parents = True, exist_ok = True)

    def run_code(self, path):
        path = path.with_suffix(".py")
        existuje = self.check_file(path)
        if not existuje:
            return None
        else:
            pass

        print("----------------------- RESULT -----------------------")
        je_frozen = getattr(sys, 'frozen', False)
        if je_frozen:
            subprocess.run(["python", str(path)])
        else:
            subprocess.run([sys.executable, str(path)])



def compile_print(path):
    tokenizer = Tokenizer()
    parser = Parser()
    transpiler = Transpiler()
    compiler = Compiler(tokenizer, parser, transpiler)
    compiler.compile(path)

def main():
    compile_print(input("Enter path to .print file: "))

if __name__ == "__main__":
    main()
else:
    pass

