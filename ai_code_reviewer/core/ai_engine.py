import requests
import json
import re
OLLAMA_URL = 'http://localhost:11434/api/generate'

class AIEngine:

    def __init__(self, model: str='mistral:7b-instruct-q4_0'):
        '''"""Summary of the function.

Args:
    self: Description of self.
    model: Description of model.

"""'''
        self.model = model

    def analyze_code(self, code: str) -> dict:
        '''"""Summary of the function.

Args:
    self: Description of self.
    code: Description of code.

Returns:
    dict: Description of return value.

"""'''
        trimmed_code = code[:1200]
        prompt = f'\nFind at least one improvement in this Python code.\n\nReturn ONLY valid JSON in this format:\n{{"semantic_issues":[],"improvements":["Always return at least one improvement"],"docstring":"","security_notes":[]}}\n\nCode:\n{trimmed_code}\n'
        payload = {'model': self.model, 'prompt': prompt, 'stream': False, 'options': {'num_predict': 200, 'temperature': 0.2}}
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=120)
            response.raise_for_status()
            raw = response.json().get('response', '')
            return self._safe_json_parse(raw)
        except Exception:
            return self._empty_response()

    def _safe_json_parse(self, raw_output: str) -> dict:
        '''"""Summary of the function.

Args:
    self: Description of self.
    raw_output: Description of raw_output.

Returns:
    dict: Description of return value.

"""'''
        try:
            raw_output = raw_output.strip()
            raw_output = re.sub('```json', '', raw_output, flags=re.IGNORECASE)
            raw_output = raw_output.replace('```', '')
            match = re.search('\\{.*\\}', raw_output, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return self._empty_response()

    def _empty_response(self) -> dict:
        '''"""Summary of the function.

Args:
    self: Description of self.

Returns:
    dict: Description of return value.

"""'''
        return {'semantic_issues': [], 'improvements': [], 'docstring': '', 'security_notes': []}