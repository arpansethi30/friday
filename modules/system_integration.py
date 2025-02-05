import subprocess
import os
from typing import Dict, Any, List, Optional
import applescript

class SystemIntegration:
    def __init__(self, config: Config):
        self.config = config
        self.terminal_history = []
        
    def control_system_setting(self, setting: str, value: Any) -> bool:
        """Control system settings like brightness, volume"""
        commands = {
            'brightness': lambda x: f'brightness {x}',
            'volume': lambda x: f'set volume output volume {x}',
            'keyboard_brightness': lambda x: f'keyboard brightness {x}'
        }
        if setting in commands:
            script = f'tell application "System Events" to {commands[setting](value)}'
            return self._run_applescript(script)
        return False
        
    def search_files(self, query: str, location: Optional[str] = None) -> List[str]:
        """Natural language file search"""
        base_cmd = ['mdfind']
        if location:
            base_cmd.extend(['-onlyin', location])
        base_cmd.append(query)
        
        try:
            result = subprocess.run(base_cmd, capture_output=True, text=True)
            return result.stdout.strip().split('\n')
        except Exception:
            return []
            
    def execute_terminal_command(self, command: str) -> Dict[str, Any]:
        """Execute terminal commands safely"""
        try:
            # Add safety checks and command validation here
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.terminal_history.append({
                'command': command,
                'output': result.stdout,
                'error': result.stderr,
                'success': result.returncode == 0
            })
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def get_app_context(self) -> Dict[str, Any]:
        """Get context about running applications"""
        script = '''
        tell application "System Events"
            set activeApps to name of every process where background only is false
            set frontApp to name of first process whose frontmost is true
        end tell
        '''
        result = self._run_applescript(script)
        return {
            'active_apps': result.get('activeApps', []),
            'frontmost_app': result.get('frontApp')
        }

    # ...additional methods for system integration...
