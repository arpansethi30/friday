# modules/tasks.py
import subprocess
import os
import sys
import webbrowser
from datetime import datetime
import psutil
import platform
import json
import requests
from typing import Dict, Optional
import logging
from config import Config

class TaskManager:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger('TaskManager')
        
        # Command registry with function mappings
        self.commands = {
            # System commands
            "system info": self._get_system_info,
            "battery": self._get_battery_status,
            "time": self._get_time,
            "date": self._get_date,
            "volume": self._adjust_volume,
            "brightness": self._adjust_brightness,
            "wifi": self._manage_wifi,
            "bluetooth": self._manage_bluetooth,
            
            # Application commands
            "open": self._open_application,
            "close": self._close_application,
            "quit": self._close_application,
            
            # Workspace commands
            "organize files": self._organize_files,
            "empty trash": self._empty_trash,
            
            # Dark mode and display
            "dark mode": self._toggle_dark_mode,
            
            # Audio controls
            "mute": self._toggle_mute,
            "unmute": self._toggle_mute,
            
            # System performance
            "memory usage": self._get_memory_usage,
            "cpu usage": self._get_cpu_usage,
            "disk space": self._get_disk_space,
            "network speed": self._get_network_speed,
            
            # Power management
            "sleep": self._sleep_system,
            "restart": self._restart_system,
            "shutdown": self._shutdown_system,
        }

    def execute_command(self, command: str) -> str:
        """Execute the given command and return the response"""
        try:
            command = command.lower().strip()
            
            # Check for exact command matches first
            for cmd, func in self.commands.items():
                if cmd in command:
                    return func(command)
            
            # Handle compound commands
            if "and" in command:
                responses = []
                sub_commands = command.split("and")
                for sub_cmd in sub_commands:
                    response = self.execute_command(sub_cmd.strip())
                    responses.append(response)
                return " And ".join(responses)
            
            return "Command not recognized. Please try again."
            
        except Exception as e:
            self.logger.error(f"Error executing command '{command}': {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"

    def _get_system_info(self, _: str) -> str:
        """Get detailed system information"""
        try:
            # Get macOS version
            os_ver = subprocess.check_output(["sw_vers", "-productVersion"]).decode().strip()
            
            # Get hardware info
            model = subprocess.check_output(["sysctl", "hw.model"]).decode().split(":")[1].strip()
            
            # Get CPU info
            cpu = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
            
            # Get memory info
            mem = psutil.virtual_memory()
            ram = f"{mem.total / (1024**3):.1f}GB"
            
            return f"Running macOS {os_ver} on {model}\nCPU: {cpu}\nRAM: {ram}\nMemory Usage: {mem.percent}%"
        except Exception as e:
            return f"Error getting system info: {str(e)}"

    def _get_battery_status(self, _: str) -> str:
        """Get battery status and power information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                status = "plugged in" if battery.power_plugged else "on battery"
                time_left = str(datetime.timedelta(seconds=battery.secsleft)) if battery.secsleft > 0 else "calculating"
                return f"Battery at {battery.percent}%, {status}. Time remaining: {time_left}"
            return "No battery information available"
        except Exception as e:
            return f"Error getting battery status: {str(e)}"

    def _adjust_volume(self, command: str) -> str:
        """Adjust system volume"""
        try:
            if "up" in command or "increase" in command:
                os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
                return "Volume increased"
            elif "down" in command or "decrease" in command:
                os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
                return "Volume decreased"
            elif "set" in command:
                # Extract number from command
                import re
                if match := re.search(r'(\d+)', command):
                    level = min(100, max(0, int(match.group(1))))
                    os.system(f"osascript -e 'set volume output volume {level}'")
                    return f"Volume set to {level}%"
            return "Please specify up, down, or set volume to a number"
        except Exception as e:
            return f"Error adjusting volume: {str(e)}"

    def _toggle_dark_mode(self, _: str) -> str:
        """Toggle system dark mode"""
        try:
            script = '''
            tell application "System Events"
                tell appearance preferences
                    set dark mode to not dark mode
                end tell
            end tell
            '''
            subprocess.run(['osascript', '-e', script], capture_output=True)
            return "Dark mode toggled"
        except Exception as e:
            return f"Error toggling dark mode: {str(e)}"

    def _manage_wifi(self, command: str) -> str:
        """Manage WiFi connection"""
        try:
            if "status" in command:
                result = subprocess.check_output(["networksetup", "-getairportnetwork", "en0"]).decode()
                return result.replace("Current Wi-Fi Network: ", "Connected to: ")
            elif "on" in command:
                subprocess.run(["networksetup", "-setairportpower", "en0", "on"])
                return "WiFi turned on"
            elif "off" in command:
                subprocess.run(["networksetup", "-setairportpower", "en0", "off"])
                return "WiFi turned off"
            return "Please specify on, off, or status"
        except Exception as e:
            return f"Error managing WiFi: {str(e)}"

    def _manage_bluetooth(self, command: str) -> str:
        """Manage Bluetooth connection"""
        try:
            if "on" in command:
                os.system("blueutil -p 1")
                return "Bluetooth turned on"
            elif "off" in command:
                os.system("blueutil -p 0")
                return "Bluetooth turned off"
            return "Please specify on or off"
        except Exception as e:
            return f"Error managing Bluetooth: {str(e)}"

    def _get_memory_usage(self, _: str) -> str:
        """Get detailed memory usage information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return (f"Memory Usage:\n"
                   f"Total: {memory.total / (1024**3):.1f}GB\n"
                   f"Used: {memory.used / (1024**3):.1f}GB ({memory.percent}%)\n"
                   f"Free: {memory.free / (1024**3):.1f}GB\n"
                   f"Swap Used: {swap.used / (1024**3):.1f}GB")
        except Exception as e:
            return f"Error getting memory usage: {str(e)}"

    def _get_cpu_usage(self, _: str) -> str:
        """Get CPU usage information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            overall = sum(cpu_percent) / len(cpu_percent)
            
            response = f"Overall CPU Usage: {overall:.1f}%\n"
            for i, cpu in enumerate(cpu_percent):
                response += f"Core {i+1}: {cpu:.1f}%\n"
            return response
        except Exception as e:
            return f"Error getting CPU usage: {str(e)}"

    def _get_disk_space(self, _: str) -> str:
        """Get disk space information"""
        try:
            disk = psutil.disk_usage('/')
            return (f"Disk Space:\n"
                   f"Total: {disk.total / (1024**3):.1f}GB\n"
                   f"Used: {disk.used / (1024**3):.1f}GB ({disk.percent}%)\n"
                   f"Free: {disk.free / (1024**3):.1f}GB")
        except Exception as e:
            return f"Error getting disk space: {str(e)}"

    def _empty_trash(self, _: str) -> str:
        """Empty the system trash"""
        try:
            os.system("rm -rf ~/.Trash/*")
            return "Trash emptied successfully"
        except Exception as e:
            return f"Error emptying trash: {str(e)}"

    def _toggle_mute(self, command: str) -> str:
        """Toggle system audio mute"""
        try:
            if "unmute" in command:
                os.system("osascript -e 'set volume output muted false'")
                return "Audio unmuted"
            else:
                os.system("osascript -e 'set volume output muted true'")
                return "Audio muted"
        except Exception as e:
            return f"Error toggling mute: {str(e)}"

    def _sleep_system(self, _: str) -> str:
        """Put the system to sleep"""
        try:
            os.system("pmset sleepnow")
            return "Putting system to sleep"
        except Exception as e:
            return f"Error putting system to sleep: {str(e)}"

    def _get_time(self, _: str) -> str:
        """Get current time"""
        return datetime.now().strftime("It's %I:%M %p")

    def _get_date(self, _: str) -> str:
        """Get current date"""
        return datetime.now().strftime("Today is %A, %B %d, %Y")

    def _adjust_brightness(self, command: str) -> str:
        """Adjust screen brightness"""
        try:
            if "up" in command or "increase" in command:
                os.system("brightness 0.1")
                return "Brightness increased"
            elif "down" in command or "decrease" in command:
                os.system("brightness -0.1")
                return "Brightness decreased"
            return "Please specify increase or decrease brightness"
        except Exception as e:
            return f"Error adjusting brightness: {str(e)}"

    def _open_application(self, command: str) -> str:
        """Open specified application"""
        try:
            # Extract app name from command
            app_name = command.split("open")[-1].strip()
            os.system(f"open -a '{app_name}'")
            return f"Opening {app_name}"
        except Exception as e:
            return f"Error opening application: {str(e)}"

    def _close_application(self, command: str) -> str:
        """Close specified application"""
        try:
            # Extract app name from command
            app_name = command.split("close")[-1].strip()
            os.system(f"osascript -e 'quit app \"{app_name}\"'")
            return f"Closing {app_name}"
        except Exception as e:
            return f"Error closing application: {str(e)}"

    def _organize_files(self, _: str) -> str:
        """Organize files on desktop by type"""
        try:
            desktop = os.path.expanduser("~/Desktop")
            categories = {
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
                'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
                'Code': ['.py', '.js', '.html', '.css', '.java'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
            }
            
            for category, extensions in categories.items():
                category_path = os.path.join(desktop, category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                    
                for file in os.listdir(desktop):
                    if any(file.lower().endswith(ext) for ext in extensions):
                        old_path = os.path.join(desktop, file)
                        new_path = os.path.join(category_path, file)
                        os.rename(old_path, new_path)
                        
            return "Desktop organized by file types"
        except Exception as e:
            return f"Error organizing files: {str(e)}"

    def _get_network_speed(self, _: str) -> str:
        """Get current network speed"""
        try:
            import speedtest
            st = speedtest.Speedtest()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            
            return f"Network Speed:\nDownload: {download_speed:.1f} Mbps\nUpload: {upload_speed:.1f} Mbps"
        except Exception as e:
            return f"Error testing network speed: {str(e)}"
        
    def _restart_system(self, _: str) -> str:
        """Restart the system"""
        try:
            os.system("osascript -e 'tell app \"System Events\" to restart'")
            return "Restarting system..."
        except Exception as e:
            return f"Error restarting system: {str(e)}"

    def _shutdown_system(self, _: str) -> str:
        """Shutdown the system"""
        try:
            os.system("osascript -e 'tell app \"System Events\" to shut down'")
            return "Shutting down system..."
        except Exception as e:
            return f"Error shutting down system: {str(e)}"