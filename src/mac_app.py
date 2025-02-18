import os
import sys
import logging
import rumps
import keyboard
from pathlib import Path
import asyncio
from threading import Thread
import subprocess

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/Library/Logs/Friday/app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Friday')

class FridayApp(rumps.App):
    def __init__(self):
        try:
            # Get the app's resource path
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, '../Resources/friday.icns')
            logger.info(f"Icon path: {icon_path}")
            
            super(FridayApp, self).__init__(
                "Friday",
                icon=icon_path if os.path.exists(icon_path) else None
            )
            
            # Initialize components
            self._setup_menu()
            self._initialize_friday()
            self._setup_hotkey()
            
            logger.info("Friday app initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Friday app: {e}", exc_info=True)
            raise

    def _setup_menu(self):
        try:
            self.menu = [
                rumps.MenuItem("Start Listening", callback=self.toggle_listening),
                rumps.MenuItem("Open Dashboard", callback=self.open_dashboard),
                None,  # Separator
                rumps.MenuItem("Preferences", callback=self.open_preferences),
                rumps.MenuItem("Check Status", callback=self.check_status)
            ]
        except Exception as e:
            logger.error(f"Error setting up menu: {e}", exc_info=True)

    def _initialize_friday(self):
        try:
            # Import Friday here to avoid circular imports
            from core import Friday
            self.friday = Friday()
            self.active = False
            
            # Start background process
            self.friday_thread = Thread(target=self._run_friday_core)
            self.friday_thread.daemon = True
            self.friday_thread.start()
        except Exception as e:
            logger.error(f"Error initializing Friday core: {e}", exc_info=True)

    def _run_friday_core(self):
        """Run Friday core in background"""
        asyncio.run(self.friday.start())

    def _setup_hotkey(self):
        try:
            # Register global hotkey
            keyboard.add_hotkey('cmd+shift+space', self.activate_friday)
        except Exception as e:
            logger.error(f"Error setting up hotkey: {e}", exc_info=True)

    def activate_friday(self):
        """Handle hotkey activation"""
        if not self.active:
            subprocess.run(["say", "Friday listening"])
            self.active = True
            # Trigger voice recognition
            asyncio.create_task(self.friday.voice.start_listening())

    @rumps.clicked("Start Listening")
    def toggle_listening(self, _):
        """Toggle listening state"""
        if self.active:
            self.menu["Start Listening"].title = "Start Listening"
            self.active = False
        else:
            self.menu["Start Listening"].title = "Stop Listening"
            self.active = True
            self.activate_friday()

    @rumps.clicked("Open Dashboard")
    def open_dashboard(self, _):
        """Open Friday dashboard"""
        subprocess.run(["open", "dashboard.html"])

    def check_status(self, _):
        """Check Friday's system status"""
        status = asyncio.run(self.friday.system.get_status())
        rumps.notification(
            title="Friday Status",
            subtitle="System Health",
            message=f"CPU: {status['cpu']}% | Memory: {status['memory']}% | Battery: {status['battery']}%"
        )

    def open_preferences(self, _):
        """Open preferences window"""
        subprocess.run(["open", "preferences.html"])

def main():
    try:
        logger.info("Starting Friday application")
        FridayApp().run()
    except Exception as e:
        logger.error(f"Critical error in Friday app: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
