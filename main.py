# main.py
import sys
import time
import random
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from modules.speech import Speech
from modules.tasks import TaskManager
from modules.memory import Memory
from modules.mac_automation import MacAutomation
from modules.personality import Personality
from modules.brain import Brain
from config import Config
from features.ai_core import AICore
from features.system_control import SystemController
from features.home_automation import HomeAutomation
from features.vision import VisionSystem  # Add this import
from modules.communication_manager import CommunicationManager
from modules.web_assistant import WebAssistant

# Remove unused imports and simplify warnings
import warnings
warnings.filterwarnings("ignore")

# Add missing class definitions
class PersonalMemory:
    def __init__(self, config):
        self.config = config
        
    def learn_from_interaction(self, data):
        # Implement learning logic
        pass

class InteractionLogger:
    def __init__(self, config):
        self.config = config
        
    def log_command(self, command, success, response):
        # Implement logging logic
        pass

# Fix FRIDAY class inheritance
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
            self.ai_core = AICore()
            self.system_controller = SystemController()
            self.vision_system = VisionSystem()
            self.home_automation = HomeAutomation()
            self.comm_manager = CommunicationManager(self.config)
            self.web_assistant = WebAssistant(self.config)
            self.personal_memory = PersonalMemory(self.config)
            self.interaction_logger = InteractionLogger(self.config)
            
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
                    
                    if text:
                        print(f"\nYou said: {text}")
                    
                    if text and self.config.WAKE_WORD.lower() in text.lower():
                        # Acknowledge wake word
                        self.speech.speak(random.choice(self.acknowledgments))
                        
                        # Listen for command
                        command = self.speech.listen_and_transcribe()
                        
                        if command:
                            print(f"You said: {command}")
                            # Process command through brain for understanding
                            intent, entities, confidence = self.brain.process_input(command)
                            
                            # Execute command
                            response = self.handle_command(command)
                            
                            # Add personality to response
                            context = self.brain.get_conversation_context()
                            personalized_response = self.personality.generate_response(response, context)
                            
                            # Speak response
                            self.speech.speak(personalized_response)
                            print(f"Friday: {personalized_response}")
                            
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
        try:
            # Process command
            response = self._base_handle_command(command)
            
            # Log the interaction
            self.interaction_logger.log_command(command, True, response)
            
            # Learn from interaction
            self.personal_memory.learn_from_interaction({
                'topic': 'command_execution',
                'data': {
                    'command': command,
                    'response': response,
                    'context': self.brain.get_conversation_context()
                },
                'source': 'command_handler',
                'confidence': 0.8
            })
            
            return response
            
        except Exception as e:
            self.interaction_logger.log_command(command, False, str(e))
            return f"Error: {str(e)}"

    def _base_handle_command(self, command: str) -> str:
        """Base handle_command implementation"""
        try:
            cmd = command.lower().strip()
            
            # Improve workspace setup command recognition
            if any(phrase in cmd for phrase in ["setup workspace", "set up workspace", "setup development", "setup coding"]):
                return self.mac.workspace_management("coding")
                
            # Add workspace setup handling
            if "setup" in cmd and "workspace" in cmd:
                if "coding" in cmd or "development" in cmd:
                    return self.mac.workspace_management("coding")
                elif "writing" in cmd:
                    return self.mac.workspace_management("writing")
                elif "research" in cmd:
                    return self.mac.workspace_management("research")
                return "Please specify workspace type (coding, writing, or research)"
            
            # Add brightness control
            if "brightness" in cmd:
                if any(word in cmd for word in ["increase", "up", "higher"]):
                    return self.mac.adjust_brightness("increase")
                elif any(word in cmd for word in ["decrease", "down", "lower"]):
                    return self.mac.adjust_brightness("decrease")
            
            # Check for open application commands
            if cmd.startswith(("open ", "launch ", "start ")):
                app_name = self._extract_app_name(cmd)
                if app_name:
                    result = self.mac.open_application(app_name)
                    return result
                return "Please specify which application to open"
                
            # Process the command
            if "email" in cmd:
                return self._handle_email_command(cmd)
            elif any(term in cmd for term in ["search", "look up", "find"]):
                return self._handle_web_search(cmd)
            elif any(keyword in cmd for keyword in ["workspace", "window", "screen", "system"]):
                return self._handle_mac_command(cmd)
            else:
                return self.tasks.execute_command(command)
                
        except Exception as e:
            self.logger.error(f"Error handling command: {e}")
            return f"I encountered an error: {str(e)}"

    def _handle_email_command(self, command: str) -> str:
        """Handle email-related commands"""
        try:
            # Check if it's a read email command
            if "check" in command and "email" in command:
                email_status = self.comm_manager.check_unread_emails()
                if "error" not in email_status:
                    unread = email_status["unread_count"]
                    urgent = len(email_status.get("urgent_messages", []))
                    return f"You have {unread} unread emails, {urgent} of them marked as urgent."
                return f"Error checking emails: {email_status['error']}"

            # Extract recipient and context
            recipient = self._extract_recipient(command)
            context = {
                'recipient': recipient,
                'intent': 'absence' if 'won\'t' in command or 'not coming' in command else 'general',
                'reason': self._extract_reason(command)
            }
            
            # Compose email
            email_data = self.comm_manager.compose_email(context)
            if 'error' in email_data:
                return f"Error composing email: {email_data['error']}"
            
            # Open in native Mail app
            if self.comm_manager.compose_mail_native(email_data):
                return f"Email drafted to {recipient} in Mail app. Please review before sending."
            return "Error creating email in Mail app"
            
        except Exception as e:
            self.logger.error(f"Error handling email command: {e}")
            return f"Error processing email command: {str(e)}"

    def _handle_web_search(self, command: str) -> str:
        """Handle web search commands"""
        try:
            # Extract search query
            query = command.replace("search", "").replace("look up", "").replace("find", "").strip()
            
            # Perform search
            results = self.web_assistant.search_and_summarize(query)
            if 'error' in results:
                return f"Error searching: {results['error']}"
            
            return results['summary']
            
        except Exception as e:
            self.logger.error(f"Error handling web search: {e}")
            return f"Error processing web search: {str(e)}"

    def _extract_recipient(self, command: str) -> str:
        """Extract recipient name from command"""
        # Basic extraction - can be enhanced with NLP
        words = command.split()
        if "to" in words:
            idx = words.index("to")
            if idx + 1 < len(words):
                return words[idx + 1]
        return ""

    def _extract_reason(self, command: str) -> str:
        """Extract reason from command"""
        # Basic extraction - can be enhanced with NLP
        if "because" in command:
            return command.split("because")[1].strip()
        return "personal reasons"

    def _handle_mac_command(self, command: str) -> str:
        """Handle Mac-specific commands"""
        try:
            # Development workflow commands
            if "setup project" in command:
                project_type = "react" if "react" in command else "python"
                name = command.split()[-1]
                return asyncio.run(self.mac.create_project_scaffold(project_type, name))
                
            # Code review workflow
            elif "review pr" in command:
                parts = command.split()
                repo_url = parts[-2]
                pr_number = parts[-1]
                return asyncio.run(self.mac.code_review_setup(repo_url, pr_number))
                
            # Meeting preparation
            elif "prepare meeting" in command:
                calendar_event = self._get_next_meeting()
                return asyncio.run(self.mac.meeting_preparation(calendar_event))
                
            # Development environment
            elif "start dev" in command:
                project_path = self._extract_project_path(command)
                return asyncio.run(self.mac.start_development_environment(project_path))
                
            # System maintenance
            elif "cleanup system" in command:
                return asyncio.run(self.mac.deep_system_cleanup())
                
            # Fall back to existing simple commands
            return self._handle_basic_mac_command(command)
            
        except Exception as e:
            self.logger.error(f"Error in Mac command handling: {e}")
            return f"I encountered an error: {str(e)}"

    def _handle_basic_mac_command(self, command: str) -> str:
        """Handle basic Mac commands (existing implementation)"""
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
        # Remove command words
        for prefix in ["open", "launch", "start"]:
            command = command.replace(prefix, "")
            
        # Clean and get the app name
        app_name = command.strip()
        
        if app_name:
            return app_name
        return None

    def _get_next_meeting(self) -> Dict[str, Any]:
        """Get next meeting details from calendar"""
        try:
            script = '''
            tell application "Calendar"
                set currentDate to current date
                set nextEvent to first event whose start date is greater than or equal to currentDate
                return {summary:summary of nextEvent, location:location of nextEvent, start date:start date of nextEvent}
            end tell
            '''
            result = self.mac.execute_system_command(script)
            if result and "Error" not in result:
                return {
                    "title": result.get("summary", "Untitled Meeting"),
                    "location": result.get("location", ""),
                    "start_time": result.get("start date", "")
                }
            return {}
        except Exception as e:
            self.logger.error(f"Error getting next meeting: {e}")
            return {}

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