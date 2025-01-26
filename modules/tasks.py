import subprocess
import os
import sys
import webbrowser
from datetime import datetime
import psutil
import platform
sys.path.append('..')
from config import Config

class TaskManager:
    def __init__(self):
        self.commands = {
            "volume": self._adjust_volume,
            "brightness": self._adjust_brightness,
            "time": self._get_time,
            "battery": self._get_battery,
            "system": self._get_system_info,
            "open": self._open_app,
            "search": self._web_search,
            "weather": self._get_weather
        }

    def execute_command(self, command):
        command = command.lower()
        
        for key, func in self.commands.items():
            if key in command:
                return func(command)
                
        return "Command not recognized. Please try again."

    def _adjust_volume(self, command):
        value = "+10" if "up" in command or "increase" in command else "-10"
        os.system(f"osascript -e 'set volume output volume (output volume of (get volume settings) {value})'")
        return "Volume adjusted"

    def _adjust_brightness(self, command):
        key = 144 if "up" in command or "increase" in command else 145
        os.system(f"osascript -e 'tell application \"System Events\" to key code {key}'")
        return "Brightness adjusted"

    def _get_time(self, _):
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    def _get_battery(self, _):
        battery = psutil.sensors_battery()
        if battery:
            return f"Battery is at {battery.percent}% {'and charging' if battery.power_plugged else ''}"
        return "Battery information unavailable"

    def _get_system_info(self, _):
        system = platform.system()
        processor = platform.processor()
        memory = psutil.virtual_memory()
        return f"Running {system} with {processor}. Memory usage: {memory.percent}%"

    def _open_app(self, command):
        apps = {
            "safari": "Safari",
            "chrome": "Google Chrome",
            "firefox": "Firefox",
            "terminal": "Terminal",
            "messages": "Messages",
            "mail": "Mail"
        }
        
        for app_keyword, app_name in apps.items():
            if app_keyword in command:
                os.system(f"open -a '{app_name}'")
                return f"Opening {app_name}"
        return "Application not found"

    def _web_search(self, command):
        search_terms = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={search_terms}"
        webbrowser.open(url)
        return f"Searching for {search_terms}"

    def _get_weather(self, _):
        # Placeholder - integrate with a weather API
        return "Weather feature coming soon. Please integrate with your preferred weather API."
