import sqlite3
from datetime import datetime
import psutil
import json
import asyncio
from collections import defaultdict

class ContextManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.pattern_cache = defaultdict(list)
        self.activity_history = []
        
    def get_current_context(self):
        context = {
            "time": datetime.now().isoformat(),
            "system_stats": self._get_system_stats(),
            "running_apps": self._get_running_apps(),
            "recent_commands": self._get_recent_commands(5),
            "recent_conversations": self._get_recent_conversations(3)
        }
        return context
    
    async def build_advanced_context(self):
        context = {
            "time_context": self._get_time_context(),
            "system_context": await self._get_system_context(),
            "workflow_context": self._get_workflow_context(),
            "patterns": self._analyze_patterns(),
            "environment": self._get_environment_state()
        }
        return context
    
    def _get_time_context(self):
        now = datetime.now()
        return {
            "time": now.isoformat(),
            "hour": now.hour,
            "day_segment": self._get_day_segment(now.hour),
            "is_worktime": self._is_worktime(now)
        }

    def _get_workflow_context(self):
        return {
            "active_project": self._detect_active_project(),
            "git_status": self._get_git_status(),
            "recent_files": self._get_recent_files(),
            "task_context": self._detect_current_task()
        }

    def _analyze_patterns(self):
        patterns = {
            "common_sequences": self._find_command_sequences(),
            "app_usage_patterns": self._analyze_app_usage(),
            "productivity_hours": self._get_productivity_patterns(),
            "frequent_workflows": self._get_common_workflows()
        }
        return patterns

    async def monitor_patterns(self):
        while True:
            current_state = await self._get_system_context()
            self.activity_history.append(current_state)
            self._update_pattern_cache()
            await asyncio.sleep(300)

    def _get_system_stats(self):
        battery = psutil.sensors_battery()
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "battery_percent": battery.percent if battery else None,
        }
    
    def _get_running_apps(self):
        return [p.name() for p in psutil.process_iter(['name'])]
    
    def _get_recent_commands(self, limit):
        cursor = self.conn.execute(
            "SELECT command, timestamp FROM command_history ORDER BY timestamp DESC LIMIT ?", 
            (limit,)
        )
        return cursor.fetchall()
    
    def _get_recent_conversations(self, limit):
        cursor = self.conn.execute(
            "SELECT user_input, response, timestamp FROM conversations ORDER BY timestamp DESC LIMIT ?", 
            (limit,)
        )
        return cursor.fetchall()
    
    def _detect_active_project(self):
        # Implement project detection logic
        pass