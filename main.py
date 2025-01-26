from modules.speech import Speech
from modules.llm import LLM
from modules.tasks import TaskManager

class FRIDAY:
    def __init__(self):
        self.speech = Speech()
        self.llm = LLM()
        self.tasks = TaskManager()
        
    def run(self):
        print("FRIDAY is online!")
        while True:
            try:
                # Listen for wake word "Friday"
                command = self.speech.listen()
                
                if "friday" in command.lower():
                    self.speech.speak("Yes, how can I help?")
                    
                    # Listen for actual command
                    task = self.speech.listen()
                    
                    # Process command through LLM
                    response = self.llm.generate(task)
                    
                    # Execute any special commands
                    if "system stats" in task.lower():
                        response = self.tasks.get_system_stats()
                    elif "screenshot" in task.lower():
                        response = self.tasks.take_screenshot()
                    elif "calculate" in task.lower():
                        query = task.replace("calculate", "").strip()
                        response = self.tasks.wolfram_query(query)
                        
                    # Respond
                    self.speech.speak(response)
                    
            except Exception as e:
                print(f"Error: {e}")
                continue

if __name__ == "__main__":
    friday = FRIDAY()
    friday.run()