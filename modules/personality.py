from typing import List, Dict
import random
from datetime import datetime
from config import Config

class Personality:
    def __init__(self, config: Config):
        self.config = config
        self.traits = config.PERSONALITY_TRAITS
        self.user_prefs = config.USER_PREFERENCES
        
    def generate_response(self, base_response: str, context: Dict) -> str:
        """Generate a personality-appropriate response"""
        # Add personality-based modifications
        response = self._add_personality_markers(base_response)
        
        # Add context-aware elements
        response = self._add_context_awareness(response, context)
        
        # Add time-appropriate greetings/closings
        response = self._add_time_awareness(response)
        
        return response
        
    def _add_personality_markers(self, text: str) -> str:
        """Add personality-specific markers to the response"""
        # Add humor if appropriate
        if self.traits["humor"] > 0.6 and random.random() < 0.3:
            text = self._add_humor(text)
            
        # Add empathy if appropriate
        if self.traits["empathy"] > 0.7:
            text = self._add_empathy(text)
            
        # Adjust formality
        text = self._adjust_formality(text)
        
        return text
        
    def _add_humor(self, text: str) -> str:
        """Add appropriate humor to responses"""
        humor_additions = [
            " I must say, handling this request is much easier than trying to understand human memes.",
            " At least this is simpler than trying to solve the meaning of life!",
            " I promise I'm not just making this up as I go... mostly.",
        ]
        
        if random.random() < 0.3:  # 30% chance to add humor
            text += random.choice(humor_additions)
            
        return text
        
    def _add_empathy(self, text: str) -> str:
        """Add empathetic elements to responses"""
        if "error" in text.lower() or "sorry" in text.lower():
            empathy_additions = [
                " I understand this might be frustrating.",
                " I'll do my best to help resolve this.",
                " Let me know if you need any clarification.",
            ]
            text += random.choice(empathy_additions)
            
        return text
        
    def _adjust_formality(self, text: str) -> str:
        """Adjust response formality based on personality settings"""
        if self.traits["formality"] > 0.7:
            # More formal replacements
            replacements = {
                "yeah": "yes",
                "nope": "no",
                "ok": "alright",
                "gonna": "going to",
                "wanna": "want to"
            }
        else:
            # More casual replacements
            replacements = {
                "certainly": "sure",
                "however": "but",
                "approximately": "about",
                "sufficient": "enough"
            }
            
        for old, new in replacements.items():
            text = text.replace(f" {old} ", f" {new} ")
            
        return text
        
    def _add_context_awareness(self, text: str, context: Dict) -> str:
        """Add context-aware elements to the response"""
        # Add user name if we have it
        if self.user_prefs["preferred_name"]:
            if random.random() < 0.3:  # 30% chance to use name
                text = f"{self.user_prefs['preferred_name']}, {text}"
                
        # Add continuation markers if in conversation
        if context.get("history", []):
            continuations = ["Also, ", "Additionally, ", "Moreover, "]
            if random.random() < 0.2:  # 20% chance to add continuation
                text = random.choice(continuations) + text.lower()
                
        return text
        
    def _add_time_awareness(self, text: str) -> str:
        """Add time-appropriate elements to the response"""
        hour = datetime.now().hour
        
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
            
        # Add greeting if it's the start of a conversation
        if text.startswith(("I can", "Here", "The", "Your")):
            text = f"{greeting}! {text}"
            
        return text