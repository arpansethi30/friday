# Complete FRIDAY AI Assistant Code Structure and Setup

# Directory Structure:
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

# Setup Commands:
mkdir -p friday/modules
cd friday
touch __init__.py main.py config.py requirements.txt
cd modules
touch __init__.py speech.py llm.py tasks.py utils.py

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
torch torchvision torchaudio
pyobjc-framework-Cocoa
pyobjc-framework-ApplicationServices

# Installation:
conda create -n friday python=3.11
conda activate friday
pip install -r requirements.txt

# All Python Code Combined:

# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
   OLLAMA_API = "http://localhost:11434/api/generate"
   MODEL = "llama2:13b"
   SYSTEM_PROMPT = """You are FRIDAY, an AI assistant. Be helpful, concise, and intelligent."""

# modules/speech.py
import whisper
import sounddevice as sd
import numpy as np
import pyttsx3
import torch

class Speech:
   def __init__(self):
       self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
       print(f"Using device: {self.device}")
       self.model = whisper.load_model("base")
       self.engine = pyttsx3.init()
       
   def listen(self, duration=3):
       try:
           print("\nListening...")
           audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='float32')
           sd.wait()
           result = self.model.transcribe(audio)
           print("Heard:", result["text"])
           return result["text"]
       except Exception as e:
           print(f"Error: {e}")
           return ""
           
   def speak(self, text):
       self.engine.say(text)
       self.engine.runAndWait()

# modules/llm.py
import requests
import sys
sys.path.append('..')
from config import Config

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
import subprocess
import os
import datetime
import sys
sys.path.append('..')
from config import Config

class TaskManager:
   def __init__(self):
       pass
       
   def get_system_stats(self):
       cpu = psutil.cpu_percent()
       memory = psutil.virtual_memory().percent
       battery = psutil.sensors_battery()
       disk = psutil.disk_usage('/')
       return f"CPU: {cpu}%, RAM: {memory}%, Disk: {disk.percent}%, Battery: {battery.percent}%"
   
   def control_volume(self, action="up"):
       script = f'set volume output volume {100 if action == "up" else 0}'
       subprocess.run(["osascript", "-e", script])
       
   def control_brightness(self, action="up"):
       script = f'tell application "System Events" to key code {144 if action == "up" else 145}'
       subprocess.run(["osascript", "-e", script])
   
   def open_application(self, app_name):
       subprocess.run(["open", "-a", app_name])
       
   def close_application(self, app_name):
       subprocess.run(["pkill", "-x", app_name])
   
   def get_calendar_events(self):
       script = '''
       tell application "Calendar"
           set today to current date
           set tomorrow to today + (24 * 60 * 60)
           get events of calendar 1 whose start date is greater than or equal to today and start date is less than tomorrow
       end tell
       '''
       try:
           result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
           return result.stdout
       except:
           return "No events found"
           
   def create_reminder(self, task, time=None):
       if not time:
           time = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H:%M")
       script = f'''
       tell application "Reminders"
           make new reminder with properties {{name:"{task}", due date:date "{time}"}}
       end tell
       '''
       subprocess.run(["osascript", "-e", script])
       
   def play_spotify(self, action="play"):
       script = f'''
       tell application "Spotify"
           {action}
       end tell
       '''
       subprocess.run(["osascript", "-e", script])
       
   def take_screenshot(self, area="full"):
       timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
       if area == "full":
           screenshot = pyautogui.screenshot()
       else:
           screenshot = pyautogui.screenshot(region=(0, 0, 300, 400))
       screenshot.save(f"screenshot_{timestamp}.png")
       return f"Screenshot saved as screenshot_{timestamp}.png"

# main.py
from modules.speech import Speech
from modules.llm import LLM
from modules.tasks import TaskManager

class FRIDAY:
   def __init__(self):
       self.speech = Speech()
       self.llm = LLM()
       self.tasks = TaskManager()
       
   def process_command(self, command):
       command = command.lower()
       
       if "volume" in command:
           action = "up" if "up" in command else "down"
           self.tasks.control_volume(action)
           return f"Volume {action}"
           
       elif "brightness" in command:
           action = "up" if "up" in command else "down"
           self.tasks.control_brightness(action)
           return f"Brightness {action}"
           
       elif "open" in command:
           app = command.split("open")[-1].strip()
           self.tasks.open_application(app)
           return f"Opening {app}"
           
       elif "close" in command:
           app = command.split("close")[-1].strip()
           self.tasks.close_application(app)
           return f"Closing {app}"
           
       elif "calendar" in command:
           return self.tasks.get_calendar_events()
           
       elif "reminder" in command:
           task = command.split("reminder")[-1].strip()
           self.tasks.create_reminder(task)
           return f"Reminder set for {task}"
           
       elif "spotify" in command:
           action = "play" if "play" in command else "pause"
           self.tasks.play_spotify(action)
           return f"Spotify {action}"
           
       elif "screenshot" in command:
           area = "selection" if "selection" in command else "full"
           return self.tasks.take_screenshot(area)
           
       elif "system" in command:
           return self.tasks.get_system_stats()
       
       return self.llm.generate(command)
   
   def run(self):
       print("FRIDAY is online! (Press Ctrl+C to exit)")
       while True:
           try:
               command = self.speech.listen()
               
               if "friday" in command.lower():
                   self.speech.speak("Yes, how can I help?")
                   task = self.speech.listen()
                   response = self.process_command(task)
                   self.speech.speak(response)
                   
           except KeyboardInterrupt:
               print("\nShutting down FRIDAY...")
               break
           except Exception as e:
               print(f"Error: {e}")
               continue

if __name__ == "__main__":
   friday = FRIDAY()
   friday.run()