import asyncio
import mlx.core as mx
import sqlite3
from datetime import datetime, timedelta

class SystemIntelligence:
    def __init__(self, config, db_path):
        self.config = config
        self.db = sqlite3.connect(db_path)
        self.predictor = SystemPredictor()
        self.optimization_threshold = config['ADVANCED_FEATURES']['system_optimization']
        
    async def monitor_system(self):
        while True:
            current_metrics = await self.get_system_metrics()
            prediction = await self.predictor.predict_system_state()
            
            if self._requires_optimization(prediction):
                await self._optimize_system_state(prediction)
                
            await self._store_metrics(current_metrics, prediction)
            await asyncio.sleep(60)
    
    async def optimize_for_workspace(self, workspace):
        resource_plan = self._calculate_resource_requirements(workspace)
        await self._prepare_system_resources(resource_plan)
        
        return {
            "cpu_priority": await self._optimize_cpu_allocation(),
            "memory_cleanup": await self._optimize_memory(),
            "power_profile": await self._set_power_profile(workspace),
            "thermal_plan": await self._manage_thermal_state()
        }
        
    async def _store_metrics(self, metrics, prediction):
        self.db.execute("""
            INSERT INTO system_metrics 
            (timestamp, metric_type, value, context, action_taken, result)
            VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
        """, (metrics['type'], metrics['value'], json.dumps(metrics['context']),
              metrics['action'], metrics['result']))
        self.db.commit()
