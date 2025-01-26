import subprocess
import psutil
import requests
import datetime
import json
import os
from config import Config
import sys
sys.path.append('..')

class TaskManager:
    def __init__(self):
        self.commands = {
            ("volume", "sound"): self._adjust_volume,
            ("brightness", "screen"): self._adjust_brightness,
            ("open", "launch", "start"): self._open_app,
            ("close", "quit"): self._close_app,
            ("status", "stats"): self._get_system_stats,
            ("time", "date"): self._get_time,
            ("weather",): self._get_weather,
            ("reminder", "remind"): self._set_reminder,
            ("search", "google", "look up"): self._web_search
        }

    def execute_command(self, command):
        if "volume" in command:
            value = "+10" if "up" in command or "increase" in command else "-10"
            os.system(f"osascript -e 'set volume output volume (output volume of (get volume settings) {value})'")
            return "Volume adjusted"
            
        elif "brightness" in command:
            key = 144 if "up" in command or "increase" in command else 145
            os.system(f"osascript -e 'tell application \"System Events\" to key code {key}'")
            return "Brightness adjusted"

    def _adjust_volume(self, command):
        direction = "up" if any(w in command for w in ["up", "increase"]) else "down"
        change = "+20" if direction == "up" else "-20"
        os.system(f"osascript -e 'set volume output volume (output volume of (get volume settings) {change})'")
        return f"Volume {direction}"

    def _adjust_brightness(self, command):
        direction = "up" if any(w in command for w in ["up", "increase"]) else "down"
        script = f'tell application "System Events" to key code {144 if direction == "up" else 145}'
        subprocess.run(["osascript", "-e", script])
        return f"Brightness {direction}"

    def _open_app(self, command):
        app = command.split("open")[-1].strip()
        subprocess.run(["open", "-a", app])
        return f"Opening {app}"

    def _close_app(self, command):
        app = command.split("close")[-1].strip()
        subprocess.run(["osascript", "-e", f'quit app "{app}"'])
        return f"Closing {app}"

    def _get_system_stats(self, _):
        stats = {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "battery": getattr(psutil.sensors_battery(), 'percent', 0)
        }
        return f"CPU: {stats['cpu']}%, Memory: {stats['memory']}%, Battery: {stats['battery']}%"

    def _get_time(self, _):
        now = datetime.datetime.now()
        return f"It's {now.strftime('%I:%M %p on %A, %B %d')}"

    def _get_weather(self, _):
        return "I'm not connected to a weather service yet"

    def _set_reminder(self, command):
        task = command.split("remind")[-1].strip()
        script = f'''
        tell application "Reminders"
            make new reminder with properties {{name:"{task}"}}
        end tell
        '''
        subprocess.run(["osascript", "-e", script])
        return f"Reminder set: {task}"

    def _web_search(self, command):
        query = command.split("search")[-1].strip()
        subprocess.run(["open", f"https://www.google.com/search?q={query}"])
        return f"Searching for {query}"

    def _ask_llm(self, prompt):
        try:
            response = requests.post(
                Config.OLLAMA_URL,
                json={"model": "llama2", "prompt": prompt}
            )
            return response.json()["response"]
        except:
            return "I'm having trouble connecting to my language model"
