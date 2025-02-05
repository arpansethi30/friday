import psutil
import sqlite3
from datetime import datetime
import subprocess
import json
import asyncio
from collections import deque
import numpy as np

class SystemMonitor:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.metrics_history = deque(maxlen=1000)
        self.anomaly_thresholds = self._load_thresholds()
        
    def track_command(self, command, output, exit_code):
        self.conn.execute(
            "INSERT INTO command_history (command, output, exit_code) VALUES (?, ?, ?)",
            (command, output, exit_code)
        )
        self.conn.commit()
    
    def track_app_usage(self, app_name, start_time):
        self.conn.execute(
            "INSERT INTO app_usage (app_name, start_time) VALUES (?, ?)",
            (app_name, start_time)
        )
        self.conn.commit()
    
    def log_system_metrics(self):
        battery = psutil.sensors_battery()
        metrics = {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "battery_level": battery.percent if battery else None,
            "temperature": psutil.sensors_temperatures().get('coretemp', [{}])[0].current
        }
        
        self.conn.execute(
            "INSERT INTO system_metrics (cpu_usage, memory_usage, battery_level, temperature) VALUES (?, ?, ?, ?)",
            (metrics["cpu_usage"], metrics["memory_usage"], metrics["battery_level"], metrics["temperature"])
        )
        self.conn.commit()
    
    async def monitor_system_advanced(self):
        while True:
            metrics = await self._get_detailed_metrics()
            self.metrics_history.append(metrics)
            
            if self._detect_anomaly(metrics):
                await self._handle_anomaly(metrics)
            
            if self._should_optimize():
                await self._optimize_system()
                
            await asyncio.sleep(60)
    
    def _detect_anomaly(self, metrics):
        predictions = self._predict_metrics()
        return self._compare_with_thresholds(metrics, predictions)
    
    async def _optimize_system(self):
        # Implement system optimization logic
        processes = self._get_resource_heavy_processes()
        for proc in processes:
            if self._should_optimize_process(proc):
                await self._optimize_process(proc)
    
    def _predict_metrics(self):
        # Implement prediction using historical data
        if len(self.metrics_history) < 10:
            return None
            
        recent_metrics = list(self.metrics_history)[-10:]
        return {
            "cpu_trend": self._calculate_trend([m["cpu_usage"] for m in recent_metrics]),
            "memory_trend": self._calculate_trend([m["memory_usage"] for m in recent_metrics]),
            "battery_trend": self._calculate_trend([m["battery_level"] for m in recent_metrics])
        }
