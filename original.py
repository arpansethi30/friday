# Project Structure
friday/
├── __init__.py
├── main.py
├── config.py
├── requirements.txt
└── modules/
    ├── __init__.py
    ├── speech.py
    ├── llm.py
    ├── tasks.py
    └── utils.py

# requirements.txt
openai-whisper
sounddevice
numpy
requests
python-dotenv
PyAudio
pyttsx3
wolframalpha
psutil
pyautogui
schedule

# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_API = "http://localhost:11434/api/generate"
    MODEL = "llama2:13b"
    SYSTEM_PROMPT = """You are FRIDAY, an AI assistant. Be helpful, concise, and intelligent."""
    WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID", "")

# modules/speech.py
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

# modules/llm.py
import requests
from ..config import Config

class LLM:
    def __init__(self):
        self.api_url = Config.OLLAMA_API
        self.model = Config.MODEL
        
    def generate(self, prompt):
        response = requests.post(
            self.api_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "system": Config.SYSTEM_PROMPT,
            }
        )
        return response.json()["response"]

# modules/tasks.py
import psutil
import pyautogui
import schedule
import wolframalpha

class TaskManager:
    def __init__(self):
        self.wolfram = wolframalpha.Client(Config.WOLFRAM_APP_ID)
        
    def get_system_stats(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        return f"CPU Usage: {cpu}%, Memory Usage: {memory}%"
        
    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return "Screenshot saved"
        
    def schedule_task(self, task, time):
        schedule.every().day.at(time).do(task)
        
    def wolfram_query(self, query):
        res = self.wolfram.query(query)
        try:
            return next(res.results).text
        except:
            return "Couldn't find an answer"

# main.py
from modules.speech import Speech
from modules.llm import LLM
from modules.tasks import TaskManager

class FRIDAY:
    def __init__(self):
        self.speech = Speech()
        self.llm = LLM()
        self.tasks = TaskManager()
        
    def run(self):
        print("FRIDAY is online!")
        while True:
            try:
                # Listen for wake word "Friday"
                command = self.speech.listen()
                
                if "friday" in command.lower():
                    self.speech.speak("Yes, how can I help?")
                    
                    # Listen for actual command
                    task = self.speech.listen()
                    
                    # Process command through LLM
                    response = self.llm.generate(task)
                    
                    # Execute any special commands
                    if "system stats" in task.lower():
                        response = self.tasks.get_system_stats()
                    elif "screenshot" in task.lower():
                        response = self.tasks.take_screenshot()
                    elif "calculate" in task.lower():
                        query = task.replace("calculate", "").strip()
                        response = self.tasks.wolfram_query(query)
                        
                    # Respond
                    self.speech.speak(response)
                    
            except Exception as e:
                print(f"Error: {e}")
                continue

if __name__ == "__main__":
    friday = FRIDAY()
    friday.run()