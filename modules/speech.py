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
        self.engine = pyttsx3.init()
        self.p = pyaudio.PyAudio()
        
        # Voice settings for macOS Samantha voice
        if sys.platform == 'darwin':  # Check if on macOS
            self.engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
        else:
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
            
        self.engine.setProperty('rate', 175)
        self.engine.setProperty('volume', 0.9)
        
    def listen_and_transcribe(self):
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
        
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        float_data = audio_data.astype(np.float32) / 32768.0
        result = self.model.transcribe(float_data)
        text = result["text"].strip().lower()
        print(f"Heard: {text}")
        return text
        
    def speak(self, text):
        print(f"FRIDAY: {text}")
        self.engine.say(text)
        self.engine.runAndWait()