import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_API = "http://localhost:11434/api/generate"
    MODEL = "llama2:13b"
    SYSTEM_PROMPT = """You are FRIDAY, an AI assistant. Be helpful, concise, and intelligent."""
    WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID", "")
