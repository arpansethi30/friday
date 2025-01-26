import whisper
import pyaudio
import numpy as np
import pyttsx3
import sys
import time
sys.path.append('..')
from config import Config

class Speech:
    def __init__(self):
        self.model = whisper.load_model(Config.WHISPER_MODEL)
        self.engine = pyttsx3.init()
        self.p = pyaudio.PyAudio()
        
        # Optimized voice settings
        self.engine.setProperty('voice', Config.VOICE_ID)
        self.engine.setProperty('rate', 175)
        self.engine.setProperty('volume', 0.9)
        
    def listen_and_transcribe(self):
        stream = self.p.open(
            format=pyaudio.paInt16,
            channels=Config.CHANNELS,
            rate=Config.SAMPLE_RATE,
            input=True,
            frames_per_buffer=Config.CHUNK_SIZE
        )
        
        frames = []
        for _ in range(0, int(Config.SAMPLE_RATE / Config.CHUNK_SIZE * Config.RECORD_SECONDS)):
            data = stream.read(Config.CHUNK_SIZE, exception_on_overflow=False)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        float_data = audio_data.astype(np.float32) / 32768.0
        result = self.model.transcribe(float_data)
        return result["text"].strip()
        
    def speak(self, text):
        print(f"FRIDAY: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
