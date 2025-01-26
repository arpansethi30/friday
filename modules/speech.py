import whisper
import sounddevice as sd
import numpy as np
import pyttsx3

class Speech:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.engine = pyttsx3.init()
        
    def listen(self, duration=5):
        print("Listening...")
        audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
        sd.wait()
        result = self.model.transcribe(audio)
        return result["text"]
    
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
