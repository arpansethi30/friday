from dataclasses import dataclass, field
from typing import Dict, List
import logging
import json
import os
from datetime import datetime

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
    
    @classmethod
    def load(cls):
        if os.path.exists(cls.CONFIG_FILE):
            with open(cls.CONFIG_FILE, 'r') as f:
                config_data = json.load(f)
                return cls(**config_data)
        return cls()
    
    def save(self):
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=4)
            
    def update_user_preferences(self, preferences: Dict[str, str]):
        self.USER_PREFERENCES.update(preferences)
        with open(self.USER_PREFS_FILE, 'w') as f:
            json.dump(self.USER_PREFERENCES, f, indent=4)