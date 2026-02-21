from pathlib import Path
from ai_code_reviewer.core.parser import CodeParser
import csv
import ast
import math

class MetricsCalculator:

    def __init__(self, path: str, exclude=None):
        '''"""Summary of the function.

Args:
    self: Description of self.
    path: Description of path.
    exclude: Description of exclude.

"""'''
        self.path = Path(path)
        self.exclude = exclude or []

    def _is_excluded(self, file_path: Path):
        '''"""Summary of the function.

Args:
    self: Description of self.
    file_path: Description of file_path.

"""'''
        for ex in self.exclude:
            if ex.rstrip('/\\') in file_path.parts:
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

    def calculate(self):
        '''"""Summary of the function.

Args:
    self: Description of self.

"""'''
        files = self._get_python_files()
        total_functions = 0
        total_classes = 0
        documented = 0
        total_complexity = 0
        for file in files:
            parser = CodeParser(str(file))
            parser.parse()
            data = parser.summary()
            total_functions += data['total_functions']
            total_classes += data['total_classes']
            documented += sum((1 for f in data['functions'] if f['has_docstring']))
            documented += sum((1 for c in data['classes'] if c['has_docstring']))
            tree = parser.tree
            file_complexity = self._calculate_complexity(tree)
            total_complexity += file_complexity
        total_items = total_functions + total_classes
        coverage = documented / total_items * 100 if total_items > 0 else 100
        avg_complexity = round(total_complexity / max(total_functions, 1), 2) if total_functions > 0 else 0
        maintainability_index = max(0, round(100 - avg_complexity * 2, 2))
        return {'files_scanned': len(files), 'total_functions': total_functions, 'total_classes': total_classes, 'coverage_percent': round(coverage, 2), 'avg_complexity': avg_complexity, 'maintainability_index': maintainability_index}

    def export_csv(self, output_path='reports/quality_report.csv'):
        '''"""Summary of the function.

Args:
    self: Description of self.
    output_path: Description of output_path.

"""'''
        result = self.calculate()
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Files Scanned', 'Total Functions', 'Total Classes', 'Coverage %'])
            writer.writerow([result['files_scanned'], result['total_functions'], result['total_classes'], result['coverage_percent']])
        return output_file

    def _calculate_complexity(self, tree):
        '''"""Summary of the function.

Args:
    self: Description of self.
    tree: Description of tree.

"""'''
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler, ast.With, ast.Try)):
                complexity += 1
        return complexity