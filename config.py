from dataclasses import dataclass, field
from typing import Dict, List
import logging
import json
import os
from pathlib import Path
from datetime import datetime
from security.encryption_utils import EncryptionManager

def default_personality_traits() -> Dict[str, float]:
    return {
        "friendliness": 0.8,
        "professionalism": 0.7,
        "humor": 0.4,
        "formality": 0.5,
        "empathy": 0.9,
        "curiosity": 0.6
    }

def default_user_preferences() -> Dict[str, str]:
    return {
        "name": "",
        "preferred_name": "",
        "location": "",
        "weather_unit": "celsius",
        "news_topics": ["technology", "science"],
        "favorite_music": [],
        "work_hours": "9:00-17:00",
        "focus_mode_apps": ["Messages", "Mail"]
    }

@dataclass
class Config:
    # Core Settings
    WHISPER_MODEL: str = "base"
    SAMPLE_RATE: int = 16000
    CHUNK_SIZE: int = 1024
    CHANNELS: int = 1
    RECORD_SECONDS: int = 3
    WAKE_WORD: str = "friday"
    VOICE_ID: str = "com.apple.speech.synthesis.voice.karen"
    
    # System Settings
    LOG_LEVEL: str = logging.INFO
    LOG_FILE: str = "friday.log"
    MEMORY_FILE: str = "memory.json"
    CONFIG_FILE: str = "config.json"
    USER_PREFS_FILE: str = "user_prefs.json"
    
    # API Keys (should be loaded from environment variables)
    WOLFRAM_ALPHA_KEY: str = field(default_factory=lambda: os.getenv('WOLFRAM_ALPHA_KEY', ''))
    NEWS_API_KEY: str = field(default_factory=lambda: os.getenv('NEWS_API_KEY', ''))
    WEATHER_API_KEY: str = field(default_factory=lambda: os.getenv('WEATHER_API_KEY', ''))
    
    # Personality Settings
    PERSONALITY_TRAITS: Dict[str, float] = field(default_factory=default_personality_traits)
    USER_PREFERENCES: Dict[str, str] = field(default_factory=default_user_preferences)
    
    # Advanced Features
    CONTEXT_MEMORY_SIZE: int = 10
    CONVERSATION_EXPIRY: int = 300  # 5 minutes
    MAX_CONVERSATION_TURNS: int = 5

    # Llama Model Settings
    OLLAMA_API: str = "http://localhost:11434/api/generate"  # Ollama API endpoint
    MODEL: str = "llama2:13b"  # Using Llama 2 13B parameter model
    SYSTEM_PROMPT: str = """You are FRIDAY, an AI assistant. Be helpful, concise, and intelligent."""

    # Directories
    PERSONAL_DATA_DIR: str = "~/.friday/personal_data"
    LOGS_DIR: str = "~/.friday/logs"
    
    # Application settings
    APP_PATHS: Dict[str, str] = field(default_factory=lambda: {
        "safari": "/Applications/Safari.app",
        "chrome": "/Applications/Google Chrome.app",
        "vscode": "/Applications/Visual Studio Code.app",
        "terminal": "/System/Applications/Utilities/Terminal.app"
    })
    
    @classmethod
    def load(cls):
        """Load configuration with conda environment support"""
        try:
            # Check if running in conda environment
            conda_prefix = os.environ.get('CONDA_PREFIX')
            if (conda_prefix):
                # Use conda environment path for logs and data
                cls.PERSONAL_DATA_DIR = os.path.join(conda_prefix, 'friday_data')
                cls.LOGS_DIR = os.path.join(conda_prefix, 'friday_logs')
                
                # Create directories if they don't exist
                os.makedirs(cls.PERSONAL_DATA_DIR, exist_ok=True)
                os.makedirs(cls.LOGS_DIR, exist_ok=True)
                
                # Update log file path
                cls.LOG_FILE = os.path.join(cls.LOGS_DIR, 'friday.log')
            
            encryption = EncryptionManager()
            
            # First try loading encrypted local config
            local_config = Path.home() / '.friday' / 'config.local.json'
            if local_config.exists():
                try:
                    encrypted_data = local_config.read_bytes()
                    config_data = encryption.decrypt(encrypted_data)
                    return cls(**config_data)
                except Exception:
                    pass
                    
            # Fall back to default config
            return cls()
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return cls()
        
    def save(self):
        encryption = EncryptionManager()
        
        # Save sensitive data to encrypted local config
        sensitive_data = {
            'USER_PREFERENCES': self.USER_PREFERENCES,
            'API_KEYS': {
                'WOLFRAM_ALPHA_KEY': self.WOLFRAM_ALPHA_KEY,
                'NEWS_API_KEY': self.NEWS_API_KEY,
                'WEATHER_API_KEY': self.WEATHER_API_KEY
            }
        }
        
        local_config = Path.home() / '.friday' / 'config.local.json'
        local_config.parent.mkdir(parents=True, exist_ok=True)
        local_config.write_bytes(encryption.encrypt(sensitive_data))
        os.chmod(str(local_config), 0o600)
        
        # Save non-sensitive data to regular config
        safe_config = {k: v for k, v in self.__dict__.items() 
                      if k not in ['USER_PREFERENCES', 'API_KEYS']}
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(safe_config, f, indent=4)
            
    def update_user_preferences(self, preferences: Dict[str, str]):
        self.USER_PREFERENCES.update(preferences)
        with open(self.USER_PREFS_FILE, 'w') as f:
            json.dump(self.USER_PREFERENCES, f, indent=4)