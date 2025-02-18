from datetime import datetime, timedelta
import json

class HealthMonitor:
    def __init__(self, config):
        self.config = config
        self.work_sessions = []
        self.break_reminders = []
        
    async def track_session(self):
        current = {
            "start_time": datetime.now(),
            "screen_time": await self._get_screen_time(),
            "posture_checks": [],
            "break_times": [],
            "caffeine_intake": []
        }
        self.work_sessions.append(current)
        
    async def check_health_metrics(self):
        return {
            "screen_time": await self._calculate_screen_time(),
            "break_needed": self._check_break_needed(),
            "posture_reminder": self._check_posture(),
            "eye_strain": self._calculate_eye_strain(),
            "next_break": self._get_next_break()
        }
        
    def suggest_break_activity(self):
        return {
            "activity": self._select_break_activity(),
            "duration": self._calculate_break_duration(),
            "exercises": self._get_relevant_exercises()
        }
