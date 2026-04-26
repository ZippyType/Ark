"""
Ark Programming Language - Batch 12: The Import System
Allowing Ark files to import other .ark files.
"""

from pathlib import Path
from lexer import tokenize
from parser import parse
from interpreter import Interpreter, Function


class Module:
    def __init__(self, name: str, symbols: dict):
        self.name = name
        self.symbols = symbols


class ImportSystem:
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.modules = {}
        self.import_stack = []
    
    def import_module(self, module_path: str) -> Module:
        path = Path(module_path)
        
        if not path.exists():
            raise ImportError(f"Module not found: {module_path}")
        
        if path.suffix != ".ark":
            raise ImportError(f"Only .ark files can be imported")
        
        source = path.read_text()
        
        old_scope = self.interpreter.current_scope
        old_idx = self.interpreter.current_scope_idx
        
        self.interpreter.global_scope.define("_module_path_", str(path.parent))
        
        program = parse(source)
        self.interpreter.interpret(program)
        
        symbols = dict(self.interpreter.global_scope.values)
        if "_module_path_" in symbols:
            del symbols["_module_path_"]
        
        module = Module(path.stem, symbols)
        self.modules[path.stem] = module
        
        self.interpreter.current_scope = old_scope
        self.interpreter.current_scope_idx = old_idx
        
        return module
    
    def import_from(self, module_path: str, names: list[str]):
        module = self.import_module(module_path)
        
        for name in names:
            if name in module.symbols:
                self.interpreter.global_scope.define(name, module.symbols[name])
            else:
                raise ImportError(f"Symbol '{name}' not found in module")


def import_file(filepath: str) -> Module:
    pass


if __name__ == "__main__":
    from interpreter import Interpreter
    
    interp = Interpreter()
    import_sys = ImportSystem(interp)
    
    print("Import system ready!")