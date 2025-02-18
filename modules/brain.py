import spacy
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
import re
from config import Config
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

class Brain:
    def __init__(self, config: Config):
        self.config = config
        self.nlp = spacy.load("en_core_web_sm")
        self.current_context = {}
        self.conversation_history = []
        self.last_interaction_time = None
        self.conversation_context = []
        self.user_preferences = self._load_preferences()
        self.learning_data_file = Path(self.config.PERSONAL_DATA_DIR) / "learning_data.json"
        self.learning_data = self._load_learning_data()
        self.logger = logging.getLogger('FRIDAY.Brain')
        
    def process_input(self, text: str) -> Tuple[str, Dict, float]:
        """
        Process user input to understand intent, entities, and context
        Returns: (intent, entities, confidence)
        """
        try:
            # Tokenize and tag parts of speech
            tokens = word_tokenize(text.lower())
            tagged = pos_tag(tokens)
            
            # Extract key information
            intent = self._determine_intent(tagged)
            entities = self._extract_entities(tagged)
            confidence = self._calculate_confidence(intent, entities)
            
            # Update conversation context
            self._update_context(text, intent, entities)
            
            return intent, entities, confidence
            
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            return "error", {}, 0.0
        
    def _determine_intent(self, tagged_tokens: List[Tuple[str, str]]) -> str:
        """Determine the user's intent from the text"""
        # Basic intent detection based on command words and sentence structure
        verbs = [word for word, tag in tagged_tokens if tag.startswith('VB')]
        nouns = [word for word, tag in tagged_tokens if tag.startswith('NN')]
        
        if not verbs:
            return "query"
            
        action = verbs[0]
        if action in ["search", "find", "look"]:
            return "search"
        elif action in ["send", "write", "email"]:
            return "email"
        elif action in ["open", "start", "launch"]:
            return "app_control"
        elif action in ["set", "change", "update"]:
            return "settings"
        
        return "general_command"
        
    def _extract_entities(self, tagged_tokens: List[Tuple[str, str]]) -> Dict:
        """Extract named entities and important information from text"""
        entities = {
            "nouns": [],
            "verbs": [],
            "adjectives": [],
            "targets": []
        }
        
        for word, tag in tagged_tokens:
            if tag.startswith('NN'):
                entities["nouns"].append(word)
            elif tag.startswith('VB'):
                entities["verbs"].append(word)
            elif tag.startswith('JJ'):
                entities["adjectives"].append(word)
                
        return entities
        
    def _calculate_confidence(self, intent: str, entities: Dict[str, List[str]]) -> float:
        """Calculate confidence score for understanding"""
        if intent == "error":
            return 0.0
            
        # Basic confidence scoring based on recognized elements
        confidence = 0.5  # Base confidence
        
        # Adjust based on intent clarity
        if intent != "general_command":
            confidence += 0.2
            
        # Adjust based on entity richness
        if entities["nouns"]:
            confidence += 0.1
        if entities["verbs"]:
            confidence += 0.1
        if entities["targets"]:
            confidence += 0.1
            
        return min(confidence, 1.0)
        
    def _update_context(self, text: str, intent: str, entities: Dict):
        """Update conversation context with new information"""
        self.conversation_context.append({
            'text': text,
            'intent': intent,
            'entities': entities,
            'timestamp': time.time()
        })
        self._trim_context()
        
    def _get_relevant_context(self) -> List[Dict]:
        """Get relevant conversation context"""
        return self.conversation_context[-5:]  # Last 5 exchanges
        
    def _analyze_with_context(self, text: str, context: List[Dict]) -> Tuple[str, Dict, float]:
        """Analyze input considering conversation context"""
        # Implementation for context-aware analysis
        pass
        
    def _learn_from_interaction(self, text: str, intent: str, entities: Dict):
        """Learn from user interactions"""
        # Update learning data based on interaction
        self.learning_data.setdefault(intent, {}).setdefault('examples', []).append(text)
        self._update_user_preferences(intent, entities)
        self._save_learning_data()
        
    def create_custom_command(self, name: str, actions: List[Dict]) -> bool:
        """Create custom voice command"""
        if name and actions:
            self.learning_data.setdefault('custom_commands', {})[name] = {
                'actions': actions,
                'created': time.time()
            }
            self._save_learning_data()
            return True
        return False
        
    def get_conversation_context(self) -> Dict:
        """Get current conversation context"""
        return {
            "current_context": self.current_context,
            "history": self.conversation_history,
            "context_age": (datetime.now() - self.last_interaction_time).seconds if self.last_interaction_time else None
        }
        
    def should_continue_conversation(self) -> bool:
        """Determine if we should continue the current conversation"""
        if not self.last_interaction_time:
            return False
            
        time_since_last = (datetime.now() - self.last_interaction_time).seconds
        return (time_since_last < self.config.CONVERSATION_EXPIRY and 
                len(self.conversation_history) < self.config.MAX_CONVERSATION_TURNS)
                
    def _load_preferences(self) -> Dict[str, Any]:
        """Load user preferences from config"""
        try:
            # First try to load from user prefs file
            prefs_path = Path(self.config.USER_PREFS_FILE)
            if prefs_path.exists():
                with open(prefs_path, 'r') as f:
                    return json.load(f)
            
            # Fall back to default preferences from config
            return self.config.USER_PREFERENCES
            
        except Exception as e:
            self.logger.error(f"Error loading preferences: {e}")
            return {}
            
    def _load_conversation_history(self) -> List[Dict[str, Any]]:
        """Load conversation history from memory file"""
        try:
            memory_path = Path(self.config.MEMORY_FILE)
            if memory_path.exists():
                with open(memory_path, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"Error loading conversation history: {e}")
            return []

    def _load_learning_data(self) -> Dict[str, Any]:
        """Load learning data from file"""
        try:
            if self.learning_data_file.exists():
                with open(self.learning_data_file, 'r') as f:
                    return json.load(f)
            
            # Initialize with default structure if file doesn't exist
            default_data = {
                'custom_commands': {},
                'learned_patterns': {},
                'user_preferences': {},
                'interaction_history': [],
                'last_updated': datetime.now().isoformat()
            }
            
            # Create directory if it doesn't exist
            self.learning_data_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Save default data
            with open(self.learning_data_file, 'w') as f:
                json.dump(default_data, f, indent=4)
                
            return default_data
            
        except Exception as e:
            self.logger.error(f"Error loading learning data: {e}")
            return {
                'custom_commands': {},
                'learned_patterns': {},
                'user_preferences': {},
                'interaction_history': [],
                'last_updated': datetime.now().isoformat()
            }

    def _save_learning_data(self):
        """Save learning data to file"""
        try:
            self.learning_data['last_updated'] = datetime.now().isoformat()
            with open(self.learning_data_file, 'w') as f:
                json.dump(self.learning_data, f, indent=4)
        except Exception as e:
            self.logger.error(f"Error saving learning data: {e}")

    def _update_user_preferences(self, intent: str, entities: Dict):
        """Update user preferences based on interaction"""
        try:
            if intent == "settings":
                for entity in entities.get('nouns', []):
                    if entity in self.user_preferences:
                        # Update preference based on command context
                        self.learning_data['user_preferences'][entity] = {
                            'value': entities.get('targets', [''])[0],
                            'last_updated': datetime.now().isoformat()
                        }
                self._save_learning_data()
        except Exception as e:
            self.logger.error(f"Error updating user preferences: {e}")
