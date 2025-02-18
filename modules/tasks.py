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
        self.logger = logging.getLogger('FRIDAY.TaskManager')
        self.command_map = {
            # System commands
            'open': self._open_application,
            'close': self._close_application,
            'brightness': self._adjust_brightness,
            'volume': self._adjust_volume,
            
            # Application commands
            'safari': self._handle_safari,
            'mail': self._handle_mail,
            'music': self._handle_music,
            
            # Workspace commands
            'workspace': self._handle_workspace,
            'focus': self._handle_focus_mode,
            
            # System controls
            'sleep': self._system_sleep,
            'restart': self._system_restart,
            'shutdown': self._system_shutdown
        }

    def execute_command(self, command: str) -> str:
        """Execute a given command"""
        try:
            # Parse command
            cmd_parts = command.lower().strip().split()
            cmd_type = cmd_parts[0] if cmd_parts else ""
            
            # Log command
            self.logger.info(f"Executing command: {command}")
            
            # Check command map
            if cmd_type in self.command_map:
                handler = self.command_map[cmd_type]
                result = handler(command)
                
                # Log result
                self.logger.info(f"Command result: {result}")
                return result
            
            return f"Command '{cmd_type}' not recognized"
            
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return f"Error executing command: {str(e)}"

    def _open_application(self, command: str) -> str:
        """Open an application"""
        try:
            app_name = command.replace('open', '').strip()
            script = f'''
                tell application "{app_name}"
                    activate
                end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return f"Opened {app_name}"
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"

    def _close_application(self, command: str) -> str:
        """Close an application"""
        try:
            app_name = command.replace('close', '').strip()
            script = f'''
                tell application "{app_name}"
                    quit
                end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return f"Closed {app_name}"
        except Exception as e:
            return f"Failed to close {app_name}: {str(e)}"

    def _adjust_brightness(self, command: str) -> str:
        """Adjust screen brightness"""
        try:
            if "increase" in command or "up" in command:
                script = 'tell application "System Events" to key code 144'
            else:
                script = 'tell application "System Events" to key code 145'
            
            subprocess.run(['osascript', '-e', script])
            return "Brightness adjusted"
        except Exception as e:
            return f"Failed to adjust brightness: {str(e)}"

    def _adjust_volume(self, command: str) -> str:
        """Adjust system volume"""
        try:
            if "increase" in command or "up" in command:
                script = '''
                    tell application "System Events"
                        set volume output volume ((output volume of (get volume settings)) + 10)
                    end tell
                '''
            else:
                script = '''
                    tell application "System Events"
                        set volume output volume ((output volume of (get volume settings)) - 10)
                    end tell
                '''
            subprocess.run(['osascript', '-e', script])
            return "Volume adjusted"
        except Exception as e:
            return f"Failed to adjust volume: {str(e)}"

    def _handle_safari(self, command: str) -> str:
        """Handle Safari-specific commands"""
        try:
            if "new tab" in command:
                script = '''
                    tell application "Safari"
                        make new document
                    end tell
                '''
            elif "close tab" in command:
                script = '''
                    tell application "Safari"
                        close current tab of window 1
                    end tell
                '''
            else:
                return "Unknown Safari command"
                
            subprocess.run(['osascript', '-e', script])
            return "Safari command executed"
        except Exception as e:
            return f"Failed to execute Safari command: {str(e)}"

    def _handle_mail(self, command: str) -> str:
        """Handle Mail-specific commands"""
        try:
            if "new email" in command:
                script = '''
                    tell application "Mail"
                        make new outgoing message
                        activate
                    end tell
                '''
            elif "check mail" in command:
                script = '''
                    tell application "Mail"
                        check for new mail
                    end tell
                '''
            else:
                return "Unknown Mail command"
                
            subprocess.run(['osascript', '-e', script])
            return "Mail command executed"
        except Exception as e:
            return f"Failed to execute Mail command: {str(e)}"

    def _handle_music(self, command: str) -> str:
        """Handle Music-specific commands"""
        try:
            if "play" in command:
                script = 'tell application "Music" to play'
            elif "pause" in command:
                script = 'tell application "Music" to pause'
            elif "next" in command:
                script = 'tell application "Music" to next track'
            elif "previous" in command:
                script = 'tell application "Music" to previous track'
            else:
                return "Unknown Music command"
                
            subprocess.run(['osascript', '-e', script])
            return "Music command executed"
        except Exception as e:
            return f"Failed to execute Music command: {str(e)}"

    def _handle_workspace(self, command: str) -> str:
        """Handle workspace commands"""
        try:
            if "coding" in command or "development" in command:
                # Extract project type if specified
                project_type = None
                if "python" in command:
                    project_type = "python"
                elif "web" in command or "react" in command:
                    project_type = "web"
                
                # Pass configuration to setup method
                config = {
                    "project_type": project_type,
                    "docs_url": None,  # Can be customized based on project
                    "terminal_count": 2 if project_type == "python" else 1
                }
                
                return self._setup_coding_workspace(config)
            elif "writing" in command:
                return self._setup_writing_workspace()
            return "Workspace type not specified"
        except Exception as e:
            return f"Failed to setup workspace: {str(e)}"

    def _setup_coding_workspace(self, config: Dict) -> str:
        """Setup coding workspace"""
        try:
            # Open VS Code
            self._open_application("Visual Studio Code")
            
            # Open Terminal
            self._open_application("Terminal")
            
            # Arrange windows
            self._arrange_windows()
            
            return "Coding workspace setup complete"
        except Exception as e:
            return f"Failed to setup coding workspace: {str(e)}"

    def _arrange_windows(self) -> None:
        """Arrange windows in workspace"""
        script = '''
            tell application "System Events"
                tell process "Visual Studio Code"
                    set position of window 1 to {0, 0}
                    set size of window 1 to {800, 900}
                end tell
                
                tell process "Terminal"
                    set position of window 1 to {801, 0}
                    set size of window 1 to {639, 900}
                end tell
            end tell
        '''
        subprocess.run(['osascript', '-e', script])

    def _handle_focus_mode(self, command: str) -> str:
        """Enable/disable focus mode"""
        try:
            if "enable" in command or "start" in command:
                for app in self.config.USER_PREFERENCES.get("focus_mode_apps", []):
                    self._close_application(f"close {app}")
                return "Focus mode enabled"
            else:
                return "Focus mode disabled"
        except Exception as e:
            return f"Failed to handle focus mode: {str(e)}"

    def _system_sleep(self, command: str) -> str:
        """Put the system to sleep"""
        try:
            script = '''
                tell application "System Events"
                    sleep
                end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return "System going to sleep"
        except Exception as e:
            return f"Failed to put system to sleep: {str(e)}"

    def _system_restart(self, command: str) -> str:
        """Restart the system"""
        try:
            script = '''
                tell application "System Events"
                    restart
                end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return "System restarting"
        except Exception as e:
            return f"Failed to restart system: {str(e)}"

    def _system_shutdown(self, command: str) -> str:
        """Shutdown the system"""
        try:
            script = '''
                tell application "System Events"
                    shut down
                end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return "System shutting down"
        except Exception as e:
            return f"Failed to shutdown system: {str(e)}"

    # Add other command handlers as needed...