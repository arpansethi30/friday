import spacy
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import re
from config import Config

class Brain:
    def __init__(self, config: Config):
        self.config = config
        self.nlp = spacy.load("en_core_web_sm")
        self.current_context = {}
        self.conversation_history = []
        self.last_interaction_time = None
        
    def process_input(self, text: str) -> Tuple[str, Dict, float]:
        """
        Process user input to understand intent, entities, and context
        Returns: (intent, entities, confidence)
        """
        doc = self.nlp(text)
        
        # Extract intent and entities
        intent = self._determine_intent(doc)
        entities = self._extract_entities(doc)
        confidence = self._calculate_confidence(doc)
        
        # Update conversation context
        self._update_context(text, intent, entities)
        
        return intent, entities, confidence
        
    def _determine_intent(self, doc) -> str:
        """Determine the user's intent from the text"""
        # Basic intent detection based on command words and sentence structure
        command_patterns = {
            "query": r"(what|who|where|when|why|how|tell me|find|search)",
            "action": r"(open|close|start|stop|set|create|delete|update)",
            "system": r"(volume|brightness|wifi|bluetooth|power|battery)",
            "reminder": r"(remind|remember|schedule|appointment)",
            "entertainment": r"(play|pause|music|video|movie)",
            "communication": r"(call|text|email|message|send)",
        }
        
        text = doc.text.lower()
        for intent, pattern in command_patterns.items():
            if re.search(pattern, text):
                return intent
                
        return "general"
        
    def _extract_entities(self, doc) -> Dict:
        """Extract named entities and important information from text"""
        entities = {}
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
            
        # Extract dates and times
        dates = []
        times = []
        for token in doc:
            if token.like_num:
                # Check if it's part of a time expression
                if any(t.text in ["am", "pm", "hour", "minute"] for t in token.children):
                    times.append(token.text)
                # Check if it's part of a date expression
                elif any(t.text in ["day", "month", "year", "week"] for t in token.children):
                    dates.append(token.text)
                    
        if dates:
            entities["dates"] = dates
        if times:
            entities["times"] = times
            
        return entities
        
    def _calculate_confidence(self, doc) -> float:
        """Calculate confidence score for understanding"""
        # Basic confidence scoring based on recognized elements
        score = 0.5  # Base confidence
        
        # Increase confidence if we recognize entities
        if doc.ents:
            score += 0.1
            
        # Increase confidence if we recognize clear command words
        command_words = ["show", "tell", "find", "open", "close", "set", "get"]
        if any(token.text.lower() in command_words for token in doc):
            score += 0.2
            
        # Increase confidence if the sentence structure is clear
        if doc[0].pos_ in ["VERB", "AUX"] and len(doc) > 2:
            score += 0.1
            
        return min(score, 1.0)
        
    def _update_context(self, text: str, intent: str, entities: Dict):
        """Update conversation context with new information"""
        current_time = datetime.now()
        
        # Check if we should start a new conversation
        if (self.last_interaction_time is None or 
            (current_time - self.last_interaction_time).seconds > self.config.CONVERSATION_EXPIRY):
            self.current_context = {}
            self.conversation_history = []
            
        # Update context
        self.current_context.update({
            "last_intent": intent,
            "last_entities": entities,
            "last_text": text,
            "timestamp": current_time.isoformat()
        })
        
        # Add to conversation history
        self.conversation_history.append({
            "text": text,
            "intent": intent,
            "entities": entities,
            "timestamp": current_time.isoformat()
        })
        
        # Trim conversation history if needed
        if len(self.conversation_history) > self.config.CONTEXT_MEMORY_SIZE:
            self.conversation_history.pop(0)
            
        self.last_interaction_time = current_time
        
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
