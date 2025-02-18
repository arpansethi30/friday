import subprocess
import os
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import applescript
import pyautogui
import json
from config import Config
import time  # Add this import at the top with other imports
import psutil
import shutil
import requests
import pyperclip
from collections import deque

class MacAutomation:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger('MacAutomation')
        self.current_workspace = None
        
    def execute_system_command(self, command: str) -> str:
        """Execute system command using osascript"""
        try:
            result = subprocess.run(['osascript', '-e', command], 
                                  capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            self.logger.error(f"Error executing system command: {e}")
            return f"Error: {str(e)}"

    def open_application(self, app_name: str) -> str:
        """Open a macOS application by name"""
        try:
            # Normalize app name
            app_mappings = {
                'safari': 'Safari',
                'chrome': 'Google Chrome',
                'firefox': 'Firefox',
                'terminal': 'Terminal',
                'vscode': 'Visual Studio Code',
                'code': 'Visual Studio Code'
                # Add more mappings as needed
            }
            
            # Get proper app name from mapping
            normalized_name = app_mappings.get(app_name.lower(), app_name)
            
            # Construct and execute AppleScript
            script = f'''
                tell application "{normalized_name}"
                    activate
                end tell
            '''
            
            proc = subprocess.Popen(['osascript', '-e', script], 
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            _, stderr = proc.communicate()
            
            if proc.returncode == 0:
                return f"Successfully opened {normalized_name}"
            else:
                error = stderr.decode('utf-8')
                self.logger.error(f"Error opening {normalized_name}: {error}")
                return f"Failed to open {normalized_name}"
                
        except Exception as e:
            self.logger.error(f"Error in open_application: {e}")
            return f"Error opening application: {str(e)}"

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
        try:
            # Open required applications
            apps_to_open = ["Visual Studio Code", "Terminal", "Safari"]
            for app in apps_to_open:
                result = self.open_application(app)
                if "Failed" in result:
                    self.logger.error(f"Failed to open {app}")
            
            # Wait for applications to launch
            time.sleep(2)  # Increased wait time for better reliability
            
            # Arrange windows in coding layout
            script = '''
                tell application "System Events"
                    delay 1
                    tell process "Code"
                        set position of window 1 to {0, 0}
                        set size of window 1 to {960, 1080}
                    end tell
                    
                    tell process "Terminal"
                        set position of window 1 to {961, 0}
                        set size of window 1 to {479, 540}
                    end tell
                    
                    tell process "Safari"
                        set position of window 1 to {961, 541}
                        set size of window 1 to {479, 539}
                    end tell
                end tell
            '''
            self.execute_system_command(script)
            
            return "Coding workspace setup complete"
            
        except Exception as e:
            self.logger.error(f"Failed to setup coding workspace: {e}")
            return f"Error setting up coding workspace: {str(e)}"

    def _setup_writing_workspace(self, data: Dict) -> str:
        """Setup writing workspace"""
        # Open preferred writing app
        self.open_application("Notes")
        self.manage_windows("maximize", "Notes")
        
        # Minimize distracting apps
        self._minimize_distracting_apps()
        
        # Enable Do Not Disturb
        self.toggle_do_not_disturb(True)
        
        return "Writing workspace setup complete"

    def _setup_research_workspace(self, data: Dict) -> str:
        """Setup research workspace"""
        # Open Safari for research
        self.open_application("Safari")
        self.manage_windows("arrange", "Safari")
        
        # Open Notes for taking notes
        self.open_application("Notes")
        self.manage_windows("arrange", "Notes")
        
        # Open specific research tools if specified
        if "research_tools" in data:
            for tool in data["research_tools"]:
                self.open_application(tool)
                
        return "Research workspace setup complete"

    def _setup_presentation_workspace(self, data: Dict) -> str:
        """Setup presentation workspace"""
        try:
            # Close distracting applications
            self._close_unnecessary_apps()
            
            # Enable Do Not Disturb
            self.toggle_do_not_disturb(True)
            
            # Clean up desktop if requested
            if data.get("clean_desktop", False):
                self._clean_desktop()
            
            # Open presentation software based on type
            if data.get("presentation_type") == "demo":
                # Setup for code demo
                self.open_application("Visual Studio Code")
                self.manage_windows("maximize", "Visual Studio Code")
                self.open_application("Terminal")
                self.manage_windows("arrange", "Terminal")
            else:
                # Setup for regular presentation
                self.open_application("Keynote")
                self.manage_windows("maximize", "Keynote")
            
            # Setup second screen if available
            self._setup_presentation_displays()
            
            return "Presentation workspace ready"
        except Exception as e:
            self.logger.error(f"Error setting up presentation: {e}")
            return f"Error setting up presentation: {str(e)}"

    def _clean_desktop(self) -> None:
        """Temporarily hide desktop icons"""
        self.execute_system_command(
            'defaults write com.apple.finder CreateDesktop false; killall Finder'
        )

    def _setup_presentation_displays(self) -> None:
        """Setup display arrangement for presentation"""
        try:
            # Check for multiple displays
            script = '''
            tell application "System Events"
                tell process "System Preferences"
                    click menu item "Displays" of menu "View" of menu bar 1
                end tell
            end tell
            '''
            self.execute_system_command(script)
            # Additional display setup can be added here
        except Exception as e:
            self.logger.error(f"Error setting up displays: {e}")

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
            self.open_application(app)
            
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
        self.open_application(meeting_app)
        
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

    async def code_review_setup(self, repo_url: str, pr_number: str) -> Dict[str, Any]:
        """Setup complete environment for code review"""
        try:
            results = {}
            # Clone/pull repository
            results["repo"] = await self._run_command(f"git clone {repo_url} review_workspace")
            
            # Checkout PR
            results["pr"] = await self._run_command(f"gh pr checkout {pr_number}")
            
            # Open VSCode with diff view
            results["editor"] = await self._run_command("code --diff HEAD^")
            
            # Open PR in browser
            results["browser"] = await self._run_command(f"gh pr view {pr_number} --web")
            
            # Start local dev environment
            results["dev_env"] = await self.start_development_environment()
            
            return {"success": True, "results": results}
        except Exception as e:
            self.logger.error(f"Code review setup failed: {e}")
            return {"success": False, "error": str(e)}

    async def meeting_preparation(self, calendar_event: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare system for an upcoming meeting"""
        try:
            # Create meeting directory if it doesn't exist
            meeting_dir = os.path.expanduser("~/Documents/MeetingNotes")
            os.makedirs(meeting_dir, exist_ok=True)
            
            # Generate meeting notes file name
            meeting_name = calendar_event.get("title", "meeting").lower().replace(" ", "_")
            notes_file = f"{meeting_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            notes_path = os.path.join(meeting_dir, notes_file)
            
            # Create and populate meeting notes
            with open(notes_path, 'w') as f:
                f.write(f"# {calendar_event.get('title', 'Meeting Notes')}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write("## Agenda\n\n## Notes\n\n## Action Items\n")
            
            # Close unnecessary applications
            await self._run_command("osascript -e 'tell application \"System Events\" to close every application not in {\"Calendar\", \"Notes\", \"zoom.us\"}'")
            
            # Open meeting notes in default editor
            os.system(f"open {notes_path}")
            
            # Set up Do Not Disturb
            self.toggle_do_not_disturb(True)
            
            # Connect to meeting if URL is available
            meeting_url = calendar_event.get("location", "")
            if any(platform in meeting_url.lower() for platform in ["zoom.us", "teams", "meet.google"]):
                os.system(f"open '{meeting_url}'")
            
            # Arrange windows
            self._setup_meeting_layout()
            
            return {
                "success": True,
                "notes_file": notes_path,
                "meeting_url": meeting_url
            }
            
        except Exception as e:
            self.logger.error(f"Meeting preparation failed: {e}")
            return {"success": False, "error": str(e)}

    async def start_development_environment(self, project_path: Optional[str] = None) -> Dict[str, Any]:
        """Start complete development environment"""
        try:
            results = {}
            
            # Start development containers if docker-compose exists
            if os.path.exists("docker-compose.yml"):
                results["docker"] = await self._run_command("docker-compose up -d")
            
            # Start database
            results["db"] = await self._run_command("brew services start postgresql")
            
            # Start required services
            services = ["redis", "elasticsearch", "mongodb"]
            for service in services:
                if self._check_service_needed(service):
                    results[service] = await self._run_command(f"brew services start {service}")
            
            # Setup IDE workspace
            results["ide"] = await self._setup_ide_workspace(project_path)
            
            # Start dev server
            if os.path.exists("package.json"):
                results["npm"] = await self._run_command("npm run dev")
            elif os.path.exists("manage.py"):
                results["django"] = await self._run_command("python manage.py runserver")
            
            return {"success": True, "results": results}
        except Exception as e:
            self.logger.error(f"Development environment setup failed: {e}")
            return {"success": False, "error": str(e)}

    async def create_project_scaffold(self, project_type: str, name: str) -> Dict[str, Any]:
        """Create new project with best practices setup"""
        try:
            results = {}
            
            if project_type == "react":
                results["create"] = await self._run_command(f"npx create-react-app {name} --template typescript")
                results["deps"] = await self._run_command("npm install @testing-library/react eslint prettier husky")
                
            elif project_type == "python":
                results["venv"] = await self._run_command(f"python -m venv {name}_env")
                results["deps"] = await self._run_command("pip install black pylint pytest")
                
            # Setup Git
            results["git"] = await self._run_command("git init")
            
            # Create GitHub repository
            results["github"] = await self._run_command(f"gh repo create {name} --private")
            
            # Setup CI/CD
            await self._setup_cicd(project_type)
            
            return {"success": True, "results": results}
        except Exception as e:
            self.logger.error(f"Project scaffold creation failed: {e}")
            return {"success": False, "error": str(e)}

    async def deep_system_cleanup(self) -> Dict[str, Any]:
        """Perform comprehensive system cleanup"""
        try:
            results = {}
            
            # Clear system caches
            results["cache"] = await self._run_command("sudo purge")
            
            # Remove unused Docker resources
            results["docker"] = await self._run_command("docker system prune -af")
            
            # Clear package manager caches
            results["brew"] = await self._run_command("brew cleanup")
            results["npm"] = await self._run_command("npm cache clean --force")
            
            # Remove old Time Machine backups
            results["timemachine"] = await self._run_command("tmutil thinLocalSnapshots / 524288000000000 4")
            
            # Empty trash
            results["trash"] = await self._run_command("rm -rf ~/.Trash/*")
            
            return {"success": True, "results": results}
        except Exception as e:
            self.logger.error(f"System cleanup failed: {e}")
            return {"success": False, "error": str(e)}

    async def _run_command(self, command: str) -> Dict[str, Any]:
        """Run shell command and return result"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "stdout": stdout.decode() if stdout else "",
                "stderr": stderr.decode() if stderr else ""
            }
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            raise

    async def _setup_meeting_layout(self):
        """Setup window layout for meetings"""
        # Implementation for arranging windows
        pass

    async def _setup_ide_workspace(self, project_path: Optional[str]) -> Dict[str, Any]:
        """Setup IDE workspace with extensions and configurations"""
        # Implementation for IDE setup
        pass

    async def _setup_cicd(self, project_type: str) -> Dict[str, Any]:
        """Setup CI/CD workflows based on project type"""
        # Implementation for CI/CD setup
        pass

    def _check_service_needed(self, service: str) -> bool:
        """Check if a service is needed for the current project"""
        # Implementation for service check
        pass

    def adjust_brightness(self, direction: str) -> str:
        """Adjust screen brightness up or down"""
        try:
            if direction.lower() == "increase":
                script = '''
                tell application "System Events"
                    key code 144  -- Increase brightness
                    key code 144
                end tell
                '''
            else:
                script = '''
                tell application "System Events"
                    key code 145  -- Decrease brightness
                    key code 145
                end tell
                '''
                
            self.execute_system_command(script)
            return f"Brightness {direction}d"
            
        except Exception as e:
            self.logger.error(f"Error adjusting brightness: {e}")
            return f"Failed to adjust brightness: {str(e)}"

    def manage_network(self, action: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Network management functions"""
        try:
            actions = {
                "wifi_toggle": self._toggle_wifi,
                "wifi_status": self._get_wifi_status,
                "ping": self._ping_host,
                "speed_test": self._run_speed_test,
                "dns_flush": self._flush_dns,
                "proxy_set": self._set_proxy,
                "scan_ports": self._scan_ports
            }
            
            if action in actions:
                return {"success": True, "result": actions[action](params)}
            return {"success": False, "error": "Invalid network action"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _toggle_wifi(self, params: Optional[Dict] = None) -> str:
        script = '''
        do shell script "networksetup -setairportpower en0 toggle"
        '''
        return self.execute_system_command(script)

    def _get_wifi_status(self, params: Optional[Dict] = None) -> Dict:
        script = '''
        do shell script "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
        '''
        return {"info": self.execute_system_command(script)}

    def _ping_host(self, params: Dict) -> Dict:
        host = params.get("host", "8.8.8.8")
        count = params.get("count", "4")
        result = subprocess.run(["ping", "-c", count, host], capture_output=True, text=True)
        return {"output": result.stdout}

    def _run_speed_test(self, params: Optional[Dict] = None) -> Dict:
        # Simple speed test using fast.com or speedtest-cli
        # Implementation would depend on preferred speed test method
        pass

    def clipboard_manager(self, action: str, data: Optional[str] = None) -> Dict[str, Any]:
        """Enhanced clipboard management"""
        try:
            if not hasattr(self, '_clipboard_history'):
                self._clipboard_history = deque(maxlen=50)  # Store last 50 items

            actions = {
                "copy": lambda: self._copy_to_clipboard(data),
                "paste": self._paste_from_clipboard,
                "clear": self._clear_clipboard,
                "history": lambda: {"history": list(self._clipboard_history)},
                "save": lambda: self._save_clipboard_to_file(data)
            }

            if action in actions:
                return {"success": True, "result": actions[action]()}
            return {"success": False, "error": "Invalid clipboard action"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _copy_to_clipboard(self, data: str) -> Dict:
        pyperclip.copy(data)
        self._clipboard_history.append(data)
        return {"copied": data}

    def _paste_from_clipboard(self) -> Dict:
        return {"content": pyperclip.paste()}

    def advanced_window_management(self, action: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Advanced window management features"""
        try:
            actions = {
                "tile_windows": self._tile_all_windows,
                "cascade_windows": self._cascade_windows,
                "center_window": self._center_current_window,
                "split_screen": self._setup_split_screen,
                "save_layout": self._save_window_layout,
                "load_layout": self._load_window_layout
            }

            if action in actions:
                return {"success": True, "result": actions[action](params)}
            return {"success": False, "error": "Invalid window action"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _tile_all_windows(self, params: Optional[Dict] = None) -> str:
        script = '''
        tell application "System Events"
            set screenSize to get size of window of desktop
            set screenWidth to item 1 of screenSize
            set screenHeight to item 2 of screenSize
            
            set windowList to every window of (every process whose visible is true)
            set windowCount to count of windowList
            
            set cols to round up of (square root of windowCount)
            set rows to round up of (windowCount / cols)
            
            set winWidth to screenWidth / cols
            set winHeight to screenHeight / rows
            
            repeat with i from 1 to windowCount
                set thisWindow to item i of windowList
                set xPos to (((i - 1) mod cols) * winWidth)
                set yPos to ((((i - 1) / cols) as integer) * winHeight)
                
                set position of thisWindow to {xPos, yPos}
                set size of thisWindow to {winWidth, winHeight}
            end repeat
        end tell
        '''
        return self.execute_system_command(script)

    def monitor_system_health(self) -> Dict[str, Any]:
        """Monitor system health metrics"""
        try:
            return {
                "cpu": self._get_cpu_stats(),
                "memory": self._get_memory_stats(),
                "disk": self._get_disk_stats(),
                "temperature": self._get_temperature(),
                "battery": self._get_battery_info(),
                "network": self._get_network_stats()
            }
        except Exception as e:
            return {"error": str(e)}

    def _get_cpu_stats(self) -> Dict:
        return {
            "percent": psutil.cpu_percent(interval=1, percpu=True),
            "freq": psutil.cpu_freq(),
            "count": psutil.cpu_count(),
            "load": os.getloadavg()
        }

    def _get_memory_stats(self) -> Dict:
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "percent": mem.percent,
            "used": mem.used,
            "free": mem.free
        }

    def power_management(self, action: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Power management features"""
        try:
            actions = {
                "sleep": self._sleep_system,
                "restart": self._restart_system,
                "shutdown": self._shutdown_system,
                "energy_profile": self._set_energy_profile,
                "battery_info": self._get_battery_info,
                "display_sleep": self._set_display_sleep
            }

            if action in actions:
                return {"success": True, "result": actions[action](params)}
            return {"success": False, "error": "Invalid power action"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _set_energy_profile(self, params: Dict) -> str:
        profile = params.get("profile", "normal")
        profiles = {
            "power_saver": "-1",
            "normal": "0",
            "performance": "1"
        }
        if profile in profiles:
            script = f'sudo pmset -a powermode {profiles[profile]}'
            return self.execute_system_command(script)
        return "Invalid power profile"

    def _set_display_sleep(self, params: Dict) -> str:
        timeout = params.get("timeout", 15)  # minutes
        script = f'sudo pmset displaysleep {timeout}'
        return self.execute_system_command(script)

    async def backup_system(self, params: Dict) -> Dict[str, Any]:
        """Perform system backup operations"""
        try:
            backup_type = params.get("type", "timemachine")
            if backup_type == "timemachine":
                return await self._start_time_machine_backup()
            elif backup_type == "custom":
                return await self._custom_backup(params)
            return {"success": False, "error": "Invalid backup type"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _start_time_machine_backup(self) -> Dict[str, Any]:
        cmd = 'tmutil startbackup'
        result = await self._run_command(cmd)
        return {"success": True, "result": result}

    async def _custom_backup(self, params: Dict) -> Dict[str, Any]:
        source = params.get("source", "~/Documents")
        destination = params.get("destination", "~/Backups")
        exclude = params.get("exclude", [])
        
        try:
            source = os.path.expanduser(source)
            destination = os.path.expanduser(destination)
            
            if not os.path.exists(destination):
                os.makedirs(destination)
                
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_path = os.path.join(destination, backup_name)
            
            shutil.copytree(source, backup_path, ignore=shutil.ignore_patterns(*exclude))
            
            return {
                "success": True,
                "backup_path": backup_path,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

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