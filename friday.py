import asyncio
import json
import logging
from pathlib import Path
from src.workspace_orchestrator import WorkspaceOrchestrator
from src.system_intelligence import SystemIntelligence
from src.context_manager import ContextManager
from src.personality import PersonalityEngine
from src.voice_handler import VoiceHandler
from src.health_monitor import HealthMonitor

class Friday:
    def __init__(self):
        self.config = self._load_config()
        self.setup_logging()
        self.initialize_components()
        
    def _load_config(self):
        config_path = Path(__file__).parent / "config/config.json"
        workspace_config_path = Path(__file__).parent / "config/workspace_config.json"
        
        with open(config_path) as f:
            config = json.load(f)
        with open(workspace_config_path) as f:
            config.update({"workspace": json.load(f)})
        return config

    def setup_logging(self):
        logging.basicConfig(
            level=self.config["LOG_LEVEL"],
            filename=self.config["LOG_FILE"],
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def initialize_components(self):
        db_path = Path(__file__).parent / "database/friday.db"
        self.context = ContextManager(db_path)
        self.workspace = WorkspaceOrchestrator(self.config, db_path)
        self.system = SystemIntelligence(self.config, db_path)
        self.personality = PersonalityEngine(self.config)
        self.voice = VoiceHandler(self.config)
        self.health = HealthMonitor(self.config)
        
    async def start(self):
        """Start Friday's main event loop"""
        print("Starting Friday AI Assistant...")
        print("Initializing components...")
        
        # Start background tasks
        tasks = [
            self.system.monitor_system(),
            self.workspace.detect_current_workspace(),
            self.health.track_session(),
            self.voice.listen_for_commands()
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print("\nShutting down Friday...")
            await self.cleanup()

    async def cleanup(self):
        """Perform cleanup operations"""
        await self.workspace.save_current_state()
        await self.system.cleanup()
        self.context.close()

if __name__ == "__main__":
    friday = Friday()
    asyncio.run(friday.start())
