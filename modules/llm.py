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

class LLM:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"  # Ollama API endpoint
        self.model = "llama2:13b"  # Using Llama 2 13B model
        self.conversation_history = []
        
    def generate(self, prompt: str) -> str:
        """Synchronous generation using local Llama through Ollama"""
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "num_ctx": 4096
                    }
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            return "I'm having trouble accessing my language model."
            
    async def generate_async(self, prompt: str) -> str:
        """Asynchronous generation using local Llama through Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "top_k": 40,
                            "num_ctx": 4096
                        }
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["response"]
                    else:
                        raise Exception(f"Ollama API error: {response.status}")
        except Exception as e:
            print(f"Error in async generation: {e}")
            return "I'm having trouble accessing my language model."