from pathlib import Path
import tomllib

class ConfigLoader:

    def __init__(self, config_path='pyproject.toml'):
        '''"""Summary of the function.

Args:
    self: Description of self.
    config_path: Description of config_path.

"""'''
        self.config_path = Path(config_path)
        self.config = {}

    def load(self):
        '''"""Summary of the function.

Args:
    self: Description of self.

"""'''
        if not self.config_path.exists():
            return {}
        with open(self.config_path, 'rb') as f:
            data = tomllib.load(f)
        return data.get('tool', {}).get('ai_code_reviewer', {})