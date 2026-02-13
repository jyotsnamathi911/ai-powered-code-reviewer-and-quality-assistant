import ast
from pathlib import Path
from ai_code_reviewer.core.generator import DocstringGenerator

class DocstringApplier(ast.NodeTransformer):

    def __init__(self, style='google'):
        '''"""Summary of the function.

Args:
    self: Description of self.
    style: Description of style.

"""'''
        self.generator = DocstringGenerator(style)

    def visit_FunctionDef(self, node):
        '''"""Summary of the function.

Args:
    self: Description of self.
    node: Description of node.

"""'''
        if ast.get_docstring(node) is None:
            func_data = {'name': node.name, 'args': [arg.arg for arg in node.args.args], 'returns': ast.unparse(node.returns) if node.returns else None}
            docstring = self.generator.generate_function_docstring(func_data)
            node.body.insert(0, ast.Expr(value=ast.Constant(value=docstring)))
        return self.generic_visit(node)

def _apply_to_file(file_path: Path, style='google'):
    '''"""Summary of the function.

Args:
    file_path: Description of file_path.
    style: Description of style.

"""'''
    source = file_path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    transformer = DocstringApplier(style)
    new_tree = transformer.visit(tree)
    updated_code = ast.unparse(new_tree)
    file_path.write_text(updated_code, encoding='utf-8')

def apply_docstrings(path: str, style='google'):
    '''"""Summary of the function.

Args:
    path: Description of path.
    style: Description of style.

"""'''
    path_obj = Path(path)
    if path_obj.is_file():
        _apply_to_file(path_obj, style)
        return
    for file in path_obj.rglob('*.py'):
        if 'venv' in file.parts:
            continue
        _apply_to_file(file, style)