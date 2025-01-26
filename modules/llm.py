import requests
import json
from typing import Dict, Any
import asyncio
import aiohttp

class EnhancedLLM:
    def __init__(self, config):
        self.config = config
        self.conversation_history = []
        self.max_history = 10
        
    async def generate_async(self, prompt: str) -> str:
        """Asynchronous generation using Ollama API"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.config.OLLAMA_API,
                json={
                    "model": self.config.MODEL,
                    "prompt": self._build_prompt(prompt),
                    "system": self.config.SYSTEM_PROMPT,
                    "stream": False
                }
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self._update_history(prompt, result["response"])
                    return result["response"]
                else:
                    raise Exception(f"API error: {response.status}")
                    
    def _build_prompt(self, current_prompt: str) -> str:
        """Build prompt with conversation history"""
        context = "\n".join([
            f"Human: {h['human']}\nAssistant: {h['assistant']}"
            for h in self.conversation_history[-self.max_history:]
        ])
        return f"{context}\nHuman: {current_prompt}"
        
    def _update_history(self, human_input: str, assistant_response: str):
        self.conversation_history.append({
            "human": human_input,
            "assistant": assistant_response
        })
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)