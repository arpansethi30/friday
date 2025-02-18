
import psutil
import asyncio
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SystemMetrics:
    cpu_percent: float
    memory_percent: float
    disk_usage: Dict[str, float]
    network_stats: Dict[str, float]
    battery_percent: Optional[float] = None
    temperature: Optional[Dict[str, float]] = None

class SystemMonitor:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('FRIDAY.SystemMonitor')
        self.metrics_history: Dict[datetime, SystemMetrics] = {}
        self.alert_thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0
        }

    async def start_monitoring(self):
        """Start continuous system monitoring"""
        while True:
            try:
                metrics = await self.get_system_metrics()
                self._store_metrics(metrics)
                await self._check_alerts(metrics)
                await asyncio.sleep(60)  # Monitor every minute
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(300)  # Back off on error

    async def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = {mount.mountpoint: psutil.disk_usage(mount.mountpoint).percent 
                   for mount in psutil.disk_partitions()}
            network = dict(psutil.net_io_counters()._asdict())
            
            metrics = SystemMetrics(
                cpu_percent=cpu,
                memory_percent=memory,
                disk_usage=disk,
                network_stats=network
            )
            
            # Add battery info if available
            if hasattr(psutil, 'sensors_battery'):
                battery = psutil.sensors_battery()
                if battery:
                    metrics.battery_percent = battery.percent

            return metrics
        except Exception as e:
            self.logger.error(f"Error getting metrics: {e}")
            raise

    async def optimize_system(self) -> Dict[str, Any]:
        """Perform system optimization tasks"""
        results = {}
        try:
            results['cache_cleared'] = await self._clear_system_caches()
            results['storage_optimized'] = await self._optimize_storage()
            results['updates_checked'] = await self._check_updates()
            return results
        except Exception as e:
            self.logger.error(f"Optimization failed: {e}")
            return {'error': str(e)}

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate system performance report"""
        try:
            return {
                'current_metrics': self.get_latest_metrics(),
                'average_metrics': self._calculate_averages(),
                'recommendations': self._generate_recommendations()
            }
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return {'error': str(e)}

    def _store_metrics(self, metrics: SystemMetrics):
        """Store metrics in history"""
        now = datetime.now()
        self.metrics_history[now] = metrics
        self._cleanup_old_metrics()

    async def _check_alerts(self, metrics: SystemMetrics):
        """Check metrics against thresholds and generate alerts"""
        alerts = []
        if metrics.cpu_percent > self.alert_thresholds['cpu_percent']:
            alerts.append(f"High CPU usage: {metrics.cpu_percent}%")
        if metrics.memory_percent > self.alert_thresholds['memory_percent']:
            alerts.append(f"High memory usage: {metrics.memory_percent}%")
        
        if alerts:
            self.logger.warning("\n".join(alerts))
            # Implement alert notification system here

    async def _clear_system_caches(self) -> bool:
        """Clear system caches"""
        # Implementation for cache clearing
        pass

    async def _optimize_storage(self) -> bool:
        """Optimize system storage"""
        # Implementation for storage optimization
        pass

    async def _check_updates(self) -> Dict[str, Any]:
        """Check for system and application updates"""
        # Implementation for update checking
        pass