import requests
response = requests.post('http://localhost:11434/api/generate', json={'model': 'mistral:7b-instruct-q4_0', 'prompt': 'Say hello in JSON format like {"test":"hello"}', 'stream': False}, timeout=30)
print(response.status_code)
print(response.json())