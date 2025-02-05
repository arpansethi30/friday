import json
from datetime import datetime
import asyncio

class PersonalityEngine:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.user_prefs = self._load_user_prefs()
        self.interaction_history = []
        self.learning_data = {}
        
    async def generate_response(self, user_input, context):
        tone = self._determine_tone(context)
        response = await self._create_response(user_input, context, tone)
        self._learn_from_interaction(user_input, response, context)
        return response
    
    def _determine_tone(self, context):
        hour = datetime.now().hour
        is_work_hours = self._is_work_hours(hour)
        return {
            "formality": self._calculate_formality(context, is_work_hours),
            "friendliness": self.config["PERSONALITY_TRAITS"]["friendliness"],
            "empathy": self._adjust_empathy(context),
            "proactiveness": self._calculate_proactiveness(context)
        }
    
    def _learn_from_interaction(self, input, response, context):
        self.interaction_history.append({
            "timestamp": datetime.now().isoformat(),
            "input": input,
            "response": response,
            "context": context,
            "feedback": None  # To be updated based on user reactions
        })
        self._update_learning_model()
