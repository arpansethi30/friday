import json
from typing import Dict, List, Any
from datetime import datetime
import os
from config import Config

class Memory:
    def __init__(self, config: Config):
        self.config = config
        self.short_term: List[Dict[str, Any]] = []
        self.long_term: Dict[str, Any] = self._load_memory()
        self.context: Dict[str, Any] = {}
        
    def _load_memory(self) -> Dict[str, Any]:
        if os.path.exists(self.config.MEMORY_FILE):
            try:
                with open(self.config.MEMORY_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
        
    def save(self):
        try:
            with open(self.config.MEMORY_FILE, 'w') as f:
                json.dump(self.long_term, f, indent=4)
        except Exception as e:
            print(f"Error saving memory: {e}")
            
    def add_interaction(self, command: str, response: str):
        self.short_term.append({
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'response': response
        })
        if len(self.short_term) > 10:
            self.short_term.pop(0)
            
    def remember_fact(self, category: str, key: str, value: Any):
        if category not in self.long_term:
            self.long_term[category] = {}
        self.long_term[category][key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        self.save()
        
    def get_context(self) -> Dict[str, Any]:
        return {
            'short_term': self.short_term[-3:],
            'context': self.context
        }