import requests
import sys
sys.path.append('..')
from config import Config

class LLM:
    def __init__(self):
        self.api_url = Config.OLLAMA_API
        self.model = Config.MODEL
        
    def generate(self, prompt):
        response = requests.post(
            self.api_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "system": Config.SYSTEM_PROMPT,
            }
        )
        return response.json()["response"]