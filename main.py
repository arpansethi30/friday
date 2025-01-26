from modules.speech import Speech
from modules.tasks import TaskManager
import time
from config import Config
from modules.speech import Speech
from modules.tasks import TaskManager


class FRIDAY:
    def __init__(self):
        print("Initializing FRIDAY...")
        self.speech = Speech()
        self.tasks = TaskManager()
        self.listening_for_command = False
        
    def run(self):
        print("FRIDAY is ready! Say 'Friday' to start.")
        
        while True:
            try:
                text = self.speech.listen_and_transcribe()
                if not text:
                    continue
                    
                if Config.WAKE_WORD in text and not self.listening_for_command:
                    self.speech.speak("Yes?")
                    self.listening_for_command = True
                    continue
                    
                if self.listening_for_command:
                    response = self.tasks.execute_command(text)
                    self.speech.speak(response)
                    self.listening_for_command = False
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                self.listening_for_command = False

if __name__ == "__main__":
    friday = FRIDAY()
    friday.run()