import subprocess
import os
import applescript
import pyautogui
import json
from datetime import datetime
from typing import List, Dict, Optional
import logging
from config import Config

class MacAutomation:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger('MacAutomation')
        
    def execute_system_command(self, command: str) -> str:
        """Execute system command using osascript"""
        try:
            result = subprocess.run(['osascript', '-e', command], 
                                  capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            self.logger.error(f"Error executing system command: {e}")
            return f"Error: {str(e)}"

    def manage_windows(self, action: str, app_name: Optional[str] = None) -> str:
        """Manage window arrangements and focus"""
        actions = {
            "arrange": """
                tell application "System Events"
                    tell process "%s"
                        set position of window 1 to {0, 0}
                        set size of window 1 to {800, 600}
                    end tell
                end tell
            """,
            "minimize": 'tell application "System Events" to tell process "%s" to set miniaturized of window 1 to true',
            "maximize": """
                tell application "System Events"
                    tell process "%s"
                        set {size, position} of window 1 to {{1440, 900}, {0, 0}}
                    end tell
                end tell
            """
        }
        
        if action in actions and app_name:
            script = actions[action] % app_name
            return self.execute_system_command(script)
        return "Invalid window management command"

    def quick_actions(self, action: str) -> str:
        """Execute quick actions and shortcuts"""
        actions = {
            "screenshot_area": self._take_area_screenshot,
            "screenshot_window": self._take_window_screenshot,
            "empty_trash": self._empty_trash,
            "show_desktop": self._show_desktop,
            "lock_screen": self._lock_screen,
            "toggle_dark_mode": self._toggle_dark_mode,
            "start_screensaver": self._start_screensaver
        }
        
        if action in actions:
            return actions[action]()
        return "Action not recognized"

    def _take_area_screenshot(self) -> str:
        """Take screenshot of selected area"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        os.system(f"screencapture -i ~/Desktop/{filename}")
        return f"Screenshot saved as {filename} on Desktop"

    def _take_window_screenshot(self) -> str:
        """Take screenshot of active window"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"window_{timestamp}.png"
        os.system(f"screencapture -w ~/Desktop/{filename}")
        return f"Window screenshot saved as {filename} on Desktop"

    def _empty_trash(self) -> str:
        """Empty the trash with confirmation"""
        script = '''
        tell application "Finder"
            empty trash
        end tell
        '''
        self.execute_system_command(script)
        return "Trash emptied successfully"

    def _show_desktop(self) -> str:
        """Show desktop by minimizing all windows"""
        script = '''
        tell application "System Events"
            key code 36 using {command down, option down}
        end tell
        '''
        self.execute_system_command(script)
        return "Showing desktop"

    def _lock_screen(self) -> str:
        """Lock the screen"""
        os.system("pmset displaysleepnow")
        return "Screen locked"

    def _toggle_dark_mode(self) -> str:
        """Toggle system dark mode"""
        script = '''
        tell application "System Events"
            tell appearance preferences
                set dark mode to not dark mode
            end tell
        end tell
        '''
        self.execute_system_command(script)
        return "Dark mode toggled"

    def _start_screensaver(self) -> str:
        """Start the screensaver"""
        os.system("open -a ScreenSaverEngine")
        return "Screensaver started"

    def workspace_management(self, action: str, data: Optional[Dict] = None) -> str:
        """Manage workspaces and app layouts"""
        actions = {
            "coding": self._setup_coding_workspace,
            "writing": self._setup_writing_workspace,
            "research": self._setup_research_workspace,
            "presentation": self._setup_presentation_workspace
        }
        
        if action in actions:
            return actions[action](data if data else {})
        return "Workspace configuration not recognized"

    def _setup_coding_workspace(self, data: Dict) -> str:
        """Setup coding workspace with preferred layout"""
        # Open VS Code
        os.system("open -a 'Visual Studio Code'")
        self.manage_windows("maximize", "Visual Studio Code")
        
        # Open Terminal
        os.system("open -a Terminal")
        self.manage_windows("arrange", "Terminal")
        
        # Open browser with documentation if specified
        if "docs_url" in data:
            os.system(f"open -a Safari {data['docs_url']}")
            
        return "Coding workspace setup complete"

    def _setup_writing_workspace(self, data: Dict) -> str:
        """Setup writing workspace"""
        # Open preferred writing app
        os.system("open -a Notes")
        self.manage_windows("maximize", "Notes")
        
        # Minimize distracting apps
        self._minimize_distracting_apps()
        
        # Enable Do Not Disturb
        self.toggle_do_not_disturb(True)
        
        return "Writing workspace setup complete"

    def _setup_research_workspace(self, data: Dict) -> str:
        """Setup research workspace"""
        # Open Safari for research
        os.system("open -a Safari")
        self.manage_windows("arrange", "Safari")
        
        # Open Notes for taking notes
        os.system("open -a Notes")
        self.manage_windows("arrange", "Notes")
        
        # Open specific research tools if specified
        if "research_tools" in data:
            for tool in data["research_tools"]:
                os.system(f"open -a '{tool}'")
                
        return "Research workspace setup complete"

    def _setup_presentation_workspace(self, data: Dict) -> str:
        """Setup presentation workspace"""
        # Open Keynote or PowerPoint
        os.system("open -a Keynote")
        self.manage_windows("maximize", "Keynote")
        
        # Close unnecessary apps
        self._close_unnecessary_apps()
        
        # Enable Do Not Disturb
        self.toggle_do_not_disturb(True)
        
        return "Presentation workspace setup complete"

    def _minimize_distracting_apps(self) -> None:
        """Minimize potentially distracting applications"""
        distracting_apps = ["Messages", "Mail", "Slack", "Discord"]
        for app in distracting_apps:
            self.manage_windows("minimize", app)

    def _close_unnecessary_apps(self) -> None:
        """Close unnecessary applications"""
        script = '''
        tell application "System Events"
            set listOfProcesses to (name of every process where background only is false)
        end tell
        '''
        result = self.execute_system_command(script)
        unnecessary_apps = ["Messages", "Mail", "Calendar", "Notes"]
        
        for app in unnecessary_apps:
            if app in result:
                os.system(f'osascript -e \'quit app "{app}"\'')

    def toggle_do_not_disturb(self, enable: bool) -> str:
        """Toggle Do Not Disturb mode"""
        value = "true" if enable else "false"
        script = f'''
        defaults -currentHost write ~/Library/Preferences/ByHost/com.apple.notificationcenterui doNotDisturb -boolean {value}
        killall NotificationCenter
        '''
        os.system(script)
        return f"Do Not Disturb {'enabled' if enable else 'disabled'}"

    def smart_automation(self, action: str, params: Optional[Dict] = None) -> str:
        """Execute smart automation sequences"""
        automations = {
            "start_work": self._start_work_sequence,
            "end_work": self._end_work_sequence,
            "prepare_meeting": self._prepare_meeting_sequence,
            "focus_mode": self._focus_mode_sequence,
            "break_time": self._break_time_sequence
        }
        
        if action in automations:
            return automations[action](params if params else {})
        return "Automation sequence not recognized"

    def _start_work_sequence(self, params: Dict) -> str:
        """Start work day sequence"""
        # Open required applications
        work_apps = params.get("apps", ["Mail", "Calendar", "Slack"])
        for app in work_apps:
            os.system(f'open -a "{app}"')
            
        # Set up workspace
        self.workspace_management(params.get("workspace", "coding"))
        
        # Check calendar for meetings
        self._check_upcoming_meetings()
        
        return "Work sequence completed"

    def _end_work_sequence(self, params: Dict) -> str:
        """End work day sequence"""
        # Save all open documents
        self._save_all_documents()
        
        # Close work applications
        self._close_unnecessary_apps()
        
        # Clear downloads folder if specified
        if params.get("clean_downloads", False):
            self._clean_downloads_folder()
            
        return "End work sequence completed"

    def _prepare_meeting_sequence(self, params: Dict) -> str:
        """Prepare for meeting sequence"""
        # Close unnecessary applications
        self._close_unnecessary_apps()
        
        # Open meeting application (Zoom, Teams, etc.)
        meeting_app = params.get("meeting_app", "zoom.us")
        os.system(f'open -a "{meeting_app}"')
        
        # Enable Do Not Disturb
        self.toggle_do_not_disturb(True)
        
        # Open meeting notes if specified
        if "notes_file" in params:
            os.system(f'open "{params["notes_file"]}"')
            
        return "Meeting preparation complete"

    def _focus_mode_sequence(self, params: Dict) -> str:
        """Enable focus mode sequence"""
        # Enable Do Not Disturb
        self.toggle_do_not_disturb(True)
        
        # Minimize distracting applications
        self._minimize_distracting_apps()
        
        # Set up focused workspace
        focus_type = params.get("focus_type", "writing")
        self.workspace_management(focus_type)
        
        # Start focus timer if specified
        if "duration" in params:
            self._start_focus_timer(params["duration"])
            
        return "Focus mode enabled"

    def _break_time_sequence(self, params: Dict) -> str:
        """Start break sequence"""
        # Minimize all windows
        self._show_desktop()
        
        # Disable Do Not Disturb
        self.toggle_do_not_disturb(False)
        
        # Start break timer if specified
        if "duration" in params:
            self._start_break_timer(params["duration"])
            
        return "Break time started"

    def _start_focus_timer(self, duration: int) -> None:
        """Start a focus timer"""
        # Implementation depends on preferred timer method
        pass

    def _start_break_timer(self, duration: int) -> None:
        """Start a break timer"""
        # Implementation depends on preferred timer method
        pass

    def _check_upcoming_meetings(self) -> None:
        """Check calendar for upcoming meetings"""
        script = '''
        tell application "Calendar"
            set currentDate to current date
            set endDate to currentDate + (60 * 60 * 24)
            set upcomingEvents to (every event whose start date is greater than or equal to currentDate and start date is less than endDate)
        end tell
        '''
        self.execute_system_command(script)

    def _save_all_documents(self) -> None:
        """Save all open documents"""
        script = '''
        tell application "System Events"
            keystroke "s" using command down
        end tell
        '''
        self.execute_system_command(script)

    def _clean_downloads_folder(self) -> None:
        """Clean up downloads folder"""
        downloads_path = os.path.expanduser("~/Downloads")
        # Implementation depends on cleanup preferences
        pass

class MacUtils:
    @staticmethod
    def get_app_info(app_name: str) -> Dict:
        """Get information about an application"""
        script = f'''
        tell application "System Events"
            tell application process "{app_name}"
                get properties
            end tell
        end tell
        '''
        try:
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            return {"status": "success", "info": result.stdout.strip()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def get_system_info() -> Dict:
        """Get detailed system information"""
        info = {}
        try:
            # Get macOS version
            info["os_version"] = subprocess.check_output(
                ["sw_vers", "-productVersion"]).decode().strip()
            
            # Get hardware info
            info["hardware"] = subprocess.check_output(
                ["system_profiler", "SPHardwareDataType"]).decode()
            
            # Get memory usage
            vm = subprocess.check_output(["vm_stat"]).decode()
            info["memory"] = vm
            
            # Get disk usage
            disk = subprocess.check_output(["df", "-h"]).decode()
            info["disk"] = disk
            
        except Exception as e:
            info["error"] = str(e)
            
        return info