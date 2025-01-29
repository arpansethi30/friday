# main.py
import sys
import time
import random
import logging
from typing import Optional
from modules.speech import Speech
from modules.tasks import TaskManager
from modules.memory import Memory
from modules.mac_automation import MacAutomation
from modules.personality import Personality
from modules.brain import Brain
from config import Config
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
class FRIDAY:
    def __init__(self):
        # Load configuration
        self.config = Config.load()
        
        # Setup logging
        logging.basicConfig(
            filename=self.config.LOG_FILE,
            level=self.config.LOG_LEVEL,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('FRIDAY')
        
        # Initialize components
        try:
            self.speech = Speech(self.config)
            self.tasks = TaskManager(self.config)
            self.memory = Memory(self.config)
            self.mac = MacAutomation(self.config)
            self.personality = Personality(self.config)
            self.brain = Brain(self.config)
            
            self.startup_phrases = [
                "Systems online. Ready to assist.",
                "All systems operational.",
                "Good day! FRIDAY at your service.",
                "FRIDAY AI initialized and ready.",
                "Online and ready to help.",
            ]
            
            self.acknowledgments = [
                "Yes?", "How can I help?", "I'm listening",
                "At your service", "What can I do for you?",
                "Ready for your command", "Waiting for instruction"
            ]
            
            self.logger.info("FRIDAY initialized successfully")
        except Exception as e:
            self.logger.error(f"Error during initialization: {e}")
            raise

    def run(self):
        """Main run loop for FRIDAY"""
        try:
            # Startup greeting
            startup_msg = random.choice(self.startup_phrases)
            self.speech.speak(startup_msg)
            
            while True:
                try:
                    # Listen for wake word
                    text = self.speech.listen_and_transcribe()
                    
                    if text and self.config.WAKE_WORD.lower() in text.lower():
                        # Acknowledge wake word
                        self.speech.speak(random.choice(self.acknowledgments))
                        
                        # Listen for command
                        command = self.speech.listen_and_transcribe()
                        
                        if command:
                            # Process command through brain for understanding
                            intent, entities, confidence = self.brain.process_input(command)
                            
                            # Execute command
                            response = self.handle_command(command)
                            
                            # Add personality to response
                            context = self.brain.get_conversation_context()
                            personalized_response = self.personality.generate_response(response, context)
                            
                            # Speak response
                            self.speech.speak(personalized_response)
                            
                            # Store in memory
                            self.memory.add_interaction(command, personalized_response)
                            
                            # Check if we should continue conversation
                            if self.brain.should_continue_conversation():
                                follow_up = self.speech.listen_and_transcribe()
                                if follow_up:
                                    self.handle_command(follow_up)
                                    
                except KeyboardInterrupt:
                    self.speech.speak("Shutting down. Goodbye!")
                    break
                except Exception as e:
                    self.logger.error(f"Error in main loop: {e}")
                    self.speech.speak("I encountered an error. Please try again.")
                    
        finally:
            # Save any pending data
            self.memory.save()
            self.config.save()
            self.logger.info("FRIDAY shutdown complete")

    def handle_command(self, command: str) -> str:
        """Handle user commands"""
        try:
            # First try Mac-specific commands
            if any(keyword in command.lower() for keyword in ["workspace", "window", "screen", "system"]):
                return self._handle_mac_command(command)
            
            # Then try regular task commands
            return self.tasks.execute_command(command)
            
        except Exception as e:
            self.logger.error(f"Error handling command: {e}")
            return f"I encountered an error: {str(e)}"

    def _handle_mac_command(self, command: str) -> str:
        """Handle Mac-specific commands"""
        # Workspace commands
        if "setup workspace" in command:
            if "coding" in command:
                return self.mac.workspace_management("coding")
            elif "writing" in command:
                return self.mac.workspace_management("writing")
            elif "research" in command:
                return self.mac.workspace_management("research")
                
        # Quick actions
        if "take screenshot" in command:
            return self.mac.quick_actions("screenshot_area")
        elif "lock screen" in command:
            return self.mac.quick_actions("lock_screen")
            
        # Smart automation sequences
        if "start work" in command:
            return self.mac.smart_automation("start_work", {
                "apps": ["Mail", "Slack", "Chrome"],
                "workspace": "coding"
            })
        elif "end work" in command:
            return self.mac.smart_automation("end_work", {
                "clean_downloads": True
            })
        elif "focus mode" in command:
            return self.mac.smart_automation("focus_mode", {
                "duration": 25,
                "focus_type": "coding"
            })
        elif "break time" in command:
            return self.mac.smart_automation("break_time", {
                "duration": 5
            })

        # Window management
        if "minimize" in command:
            app_name = self._extract_app_name(command)
            if app_name:
                return self.mac.manage_windows("minimize", app_name)
        elif "maximize" in command:
            app_name = self._extract_app_name(command)
            if app_name:
                return self.mac.manage_windows("maximize", app_name)

        # System controls
        if "dark mode" in command:
            return self.mac.quick_actions("toggle_dark_mode")
        elif "do not disturb" in command:
            enable = "on" in command or "enable" in command
            return self.mac.toggle_do_not_disturb(enable)

        return "I'm not sure how to handle that command"

    def _extract_app_name(self, command: str) -> Optional[str]:
        """Extract application name from command"""
        common_apps = {
            "safari": "Safari",
            "chrome": "Google Chrome",
            "firefox": "Firefox",
            "terminal": "Terminal",
            "vscode": "Visual Studio Code",
            "code": "Visual Studio Code",
            "notes": "Notes",
            "mail": "Mail",
            "messages": "Messages",
            "slack": "Slack",
            "zoom": "zoom.us"
        }
        
        for keyword, app_name in common_apps.items():
            if keyword in command.lower():
                return app_name
        return None

if __name__ == "__main__":
    friday = FRIDAY()
    try:
        friday.run()
    except KeyboardInterrupt:
        print("\nShutting down FRIDAY...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Goodbye!")