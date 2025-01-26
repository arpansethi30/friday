# modules/speech.py
import whisper
import pyaudio
import numpy as np
import pyttsx3
import sys
sys.path.append('..')
from config import Config

class Speech:
    def __init__(self):
        self.model = whisper.load_model(Config.WHISPER_MODEL)
        self.setup_tts()
        self.p = pyaudio.PyAudio()
        
    def setup_tts(self):
        """Initialize text-to-speech with specific settings"""
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        # Use default voice
        self.engine.setProperty('voice', voices[0].id)
        # These specific values worked well before
        self.engine.setProperty('rate', 175)  # Original working speed
        self.engine.setProperty('volume', 0.9) # Original working volume
        
    def listen_and_transcribe(self):
        # Create fresh stream each time
        stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        print("\nListening...")
        frames = []
        for _ in range(0, int(16000 / 1024 * 3)):
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        
        audio = np.frombuffer(b''.join(frames), dtype=np.int16).astype(np.float32) / 32768.0
        result = self.model.transcribe(audio)
        text = result["text"].strip().lower()
        print(f"Heard: {text}")
        return text
        
    def speak(self, text):
        """Simple, reliable speak method"""
        print(f"FRIDAY: {text}")
        self.engine.say(text)
        self.engine.runAndWait()