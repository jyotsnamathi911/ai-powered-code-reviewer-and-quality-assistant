from typing import Dict, List

class DocstringGenerator:

    def __init__(self, style: str='google'):
        '''"""Summary of the function.

Args:
    self: Description of self.
    style: Description of style.

"""'''
        self.style = style.lower()

    def generate_function_docstring(self, func: Dict) -> str:
        '''"""Summary of the function.

Args:
    self: Description of self.
    func: Description of func.

Returns:
    str: Description of return value.

"""'''
        if self.style == 'google':
            return self._google_style(func)
        elif self.style == 'numpy':
            return self._numpy_style(func)
        elif self.style == 'rest':
            return self._rest_style(func)
        else:
            raise ValueError('Unsupported docstring style')

    def _google_style(self, func: Dict) -> str:
        '''"""Summary of the function.

Args:
    self: Description of self.
    func: Description of func.

Returns:
    str: Description of return value.

"""'''
        lines: List[str] = []
        lines.append('"""Summary of the function.')
        lines.append('')
        if func['args']:
            lines.append('Args:')
            for arg in func['args']:
                lines.append(f'    {arg}: Description of {arg}.')
            lines.append('')
        if func['returns']:
            lines.append('Returns:')
            lines.append(f"    {func['returns']}: Description of return value.")
            lines.append('')
        lines.append('"""')
        return '\n'.join(lines)

    def _numpy_style(self, func: Dict) -> str:
        '''"""Summary of the function.

Args:
    self: Description of self.
    func: Description of func.

Returns:
    str: Description of return value.

"""'''
        lines: List[str] = []
        lines.append('"""Summary of the function.')
        lines.append('')
        if func['args']:
            lines.append('Parameters')
            lines.append('----------')
            for arg in func['args']:
                lines.append(f'{arg} : type')
                lines.append(f'    Description of {arg}.')
            lines.append('')
        if func['returns']:
            lines.append('Returns')
            lines.append('-------')
            lines.append(f"{func['returns']}")
            lines.append('    Description of return value.')
            lines.append('')
        lines.append('"""')
        return '\n'.join(lines)

    def _rest_style(self, func: Dict) -> str:
        '''"""Summary of the function.

Args:
    self: Description of self.
    func: Description of func.

Returns:
    str: Description of return value.

"""'''
        lines: List[str] = []
        lines.append('"""Summary of the function.')
        lines.append('')
        for arg in func['args']:
            lines.append(f':param {arg}: Description of {arg}.')
        if func['returns']:
            lines.append(f':return: Description of return value.')
            lines.append(f":rtype: {func['returns']}")
        lines.append('"""')
        return '\n'.join(lines)