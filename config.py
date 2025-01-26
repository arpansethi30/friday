import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# config.py
class Config:
    WHISPER_MODEL = "base"
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    CHANNELS = 1
    RECORD_SECONDS = 3
    WAKE_WORD = "friday"