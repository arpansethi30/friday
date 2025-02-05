import requests
import json
from typing import Dict, Tuple, Any
import logging

class AICore:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "llama2:13b"
        self.context_memory = {}
        self.logger = logging.getLogger('FRIDAY.AICore')

    def process_natural_language(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """Process text and return response with basic sentiment analysis"""
        try:
            response = self._generate_response(text)
            emotion = self._analyze_sentiment(text)
            return response, emotion
        except Exception as e:
            self.logger.error(f"Error processing text: {e}")
            return "I encountered an error processing that.", {"sentiment": "neutral"}

    def _generate_response(self, prompt: str) -> str:
        """Generate response using Ollama API"""
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ollama API error: {e}")
            return "I'm having trouble accessing my language model."

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Basic sentiment analysis using keyword matching"""
        positive_words = {"good", "great", "awesome", "excellent", "happy", "love", "wonderful"}
        negative_words = {"bad", "terrible", "awful", "sad", "hate", "poor", "wrong"}
        
        words = set(text.lower().split())
        pos_count = len(words.intersection(positive_words))
        neg_count = len(words.intersection(negative_words))
        
        if pos_count > neg_count:
            return {"sentiment": "positive", "confidence": 0.8}
        elif neg_count > pos_count:
            return {"sentiment": "negative", "confidence": 0.8}
        return {"sentiment": "neutral", "confidence": 0.5}

    def remember_context(self, conversation_id: str, context: Dict[str, Any]):
        """Store conversation context"""
        self.context_memory[conversation_id] = context

    def get_context(self, conversation_id: str) -> Dict[str, Any]:
        """Retrieve conversation context"""
        return self.context_memory.get(conversation_id, {})
