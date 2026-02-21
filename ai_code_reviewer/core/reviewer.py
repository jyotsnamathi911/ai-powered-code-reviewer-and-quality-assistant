import ast
from pathlib import Path
from .ai_engine import AIEngine

class CodeReviewer:

    def __init__(self, path: str, exclude=None, use_ai: bool=False, model: str='mistral:7b-instruct-q4_0'):
        '''"""Summary of the function.

Args:
    self: Description of self.
    path: Description of path.
    exclude: Description of exclude.
    use_ai: Description of use_ai.
    model: Description of model.

"""'''
        self.path = Path(path)
        self.exclude = exclude or []
        self.issues = []
        self.use_ai = use_ai
        self.ai_engine = AIEngine(model) if use_ai else None

    def review(self):
        '''"""Summary of the function.

Args:
    self: Description of self.

"""'''
        files = self._get_python_files()
        for file in files:
            self._review_file(file)
        return self.issues

    def _is_excluded(self, file_path):
        '''"""Summary of the function.

Args:
    self: Description of self.
    file_path: Description of file_path.

"""'''
        for ex in self.exclude:
            if ex in file_path.parts:
                return True
        return False

    def _get_python_files(self):
        '''"""Summary of the function.

Args:
    self: Description of self.

"""'''
        if self.path.is_file():
            return [self.path]
        files = []
        for file in self.path.rglob('*.py'):
            if not self._is_excluded(file):
                files.append(file)
        return files

    def _review_file(self, file_path):
        '''"""Summary of the function.

Args:
    self: Description of self.
    file_path: Description of file_path.

"""'''
        source = file_path.read_text(encoding='utf-8')
        tree = ast.parse(source)
        self._check_missing_docstrings(tree, file_path)
        self._check_long_functions(tree, file_path)
        self._check_missing_type_hints(tree, file_path)
        if self.use_ai:
            self._run_ai_review(file_path, source)

    def _run_ai_review(self, file_path, source):
        '''"""Summary of the function.

Args:
    self: Description of self.
    file_path: Description of file_path.
    source: Description of source.

"""'''
        ai_result = self.ai_engine.analyze_code(source)
        for msg in ai_result.get('semantic_issues', []):
            self.issues.append({'file': str(file_path), 'type': 'AI_Semantic', 'severity': 'info', 'line': 1, 'message': msg})
        for msg in ai_result.get('improvements', []):
            self.issues.append({'file': str(file_path), 'type': 'AI_Improvement', 'severity': 'info', 'line': 1, 'message': msg})
        for msg in ai_result.get('security_notes', []):
            self.issues.append({'file': str(file_path), 'type': 'AI_Security', 'severity': 'warning', 'line': 1, 'message': msg})

    def _check_missing_docstrings(self, tree, file_path):
        '''"""Summary of the function.

Args:
    self: Description of self.
    tree: Description of tree.
    file_path: Description of file_path.

"""'''
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if node.name.startswith('_'):
                    continue
                if ast.get_docstring(node) is None:
                    self.issues.append({'file': str(file_path), 'type': 'MissingDocstring', 'severity': 'warning', 'line': node.lineno, 'message': f'{node.name} lacks a docstring.'})

    def _check_long_functions(self, tree, file_path, max_lines=30):
        '''"""Summary of the function.

Args:
    self: Description of self.
    tree: Description of tree.
    file_path: Description of file_path.
    max_lines: Description of max_lines.

"""'''
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and hasattr(node, 'end_lineno'):
                length = node.end_lineno - node.lineno
                if length > max_lines:
                    self.issues.append({'file': str(file_path), 'type': 'LongFunction', 'severity': 'critical', 'line': node.lineno, 'message': f'{node.name} exceeds {max_lines} lines.'})

    def _check_missing_type_hints(self, tree, file_path):
        '''"""Summary of the function.

Args:
    self: Description of self.
    tree: Description of tree.
    file_path: Description of file_path.

"""'''
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.arg == 'self':
                        continue
                    if arg.annotation is None:
                        self.issues.append({'file': str(file_path), 'type': 'MissingTypeHint', 'severity': 'info', 'line': node.lineno, 'message': f'{arg.arg} in {node.name} lacks type hint.'})