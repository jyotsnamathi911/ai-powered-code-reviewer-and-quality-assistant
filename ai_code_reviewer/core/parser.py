import ast
from pathlib import Path
from typing import List, Dict, Any

class CodeParser:

    def __init__(self, file_path: str):
        '''"""Summary of the function.

Args:
    self: Description of self.
    file_path: Description of file_path.

"""'''
        self.file_path = Path(file_path)
        self.tree = None
        self.functions: List[Dict[str, Any]] = []
        self.classes: List[Dict[str, Any]] = []

    def parse(self):
        '''"""Summary of the function.

Args:
    self: Description of self.

"""'''
        with open(self.file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        self.tree = ast.parse(source)
        self._extract()

    def _extract(self):
        '''"""Summary of the function.

Args:
    self: Description of self.

"""'''
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.functions.append(self._extract_function(node))
            if isinstance(node, ast.ClassDef):
                self.classes.append(self._extract_class(node))

    def _extract_function(self, node: ast.FunctionDef) -> Dict[str, Any]:
        '''"""Summary of the function.

Args:
    self: Description of self.
    node: Description of node.

Returns:
    Dict[str, Any]: Description of return value.

"""'''
        return {'name': node.name, 'args': [arg.arg for arg in node.args.args], 'returns': ast.unparse(node.returns) if node.returns else None, 'has_docstring': ast.get_docstring(node) is not None, 'lineno': node.lineno}

    def _extract_class(self, node: ast.ClassDef) -> Dict[str, Any]:
        '''"""Summary of the function.

Args:
    self: Description of self.
    node: Description of node.

Returns:
    Dict[str, Any]: Description of return value.

"""'''
        methods = [self._extract_function(n) for n in node.body if isinstance(n, ast.FunctionDef)]
        return {'name': node.name, 'methods': methods, 'has_docstring': ast.get_docstring(node) is not None, 'lineno': node.lineno}

    def summary(self):
        '''"""Summary of the function.

Args:
    self: Description of self.

"""'''
        return {'total_functions': len(self.functions), 'total_classes': len(self.classes), 'functions': self.functions, 'classes': self.classes}