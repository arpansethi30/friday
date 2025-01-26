import sys
import time
import random
sys.path.append('.')
from modules.speech import Speech
from modules.tasks import TaskManager
from config import Config

class FRIDAY:
    def __init__(self):
        self.speech = Speech()
        self.tasks = TaskManager()
        self.startup_phrases = [
            "Systems online. Ready to assist.",
            "All systems operational.",
            "Good day! FRIDAY at your service.",
        ]
        self.acknowledgments = [
            "Yes?", "How can I help?", "I'm listening",
            "At your service", "What can I do for you?"
        ]
        
    def run(self):
        startup_msg = random.choice(self.startup_phrases)
        self.speech.speak(startup_msg)
        
        while True:
            try:
                text = self.speech.listen_and_transcribe()
                if Config.WAKE_WORD in text.lower():
                    self.speech.speak(random.choice(self.acknowledgments))
                    command = self.speech.listen_and_transcribe()
                    response = self.tasks.execute_command(command)
                    self.speech.speak(response)
            except KeyboardInterrupt:
                self.speech.speak("Shutting down. Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    friday = FRIDAY()
    friday.run()