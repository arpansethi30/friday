import psutil
import pyautogui
import schedule
import wolframalpha

class TaskManager:
    def __init__(self):
        self.wolfram = wolframalpha.Client(Config.WOLFRAM_APP_ID)
        
    def get_system_stats(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        return f"CPU Usage: {cpu}%, Memory Usage: {memory}%"
        
    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return "Screenshot saved"
        
    def schedule_task(self, task, time):
        schedule.every().day.at(time).do(task)
        
    def wolfram_query(self, query):
        res = self.wolfram.query(query)
        try:
            return next(res.results).text
        except:
            return "Couldn't find an answer"
