import os
import psutil
import subprocess

class SystemController:
    def __init__(self):
        self.monitored_apps = []

    def control_system(self, command):
        if command == "shutdown":
            os.system("shutdown /s /t 1")
        elif command == "restart":
            os.system("shutdown /r /t 1")

    def launch_application(self, app_name):
        try:
            subprocess.Popen(app_name)
            return True
        except:
            return False

    def monitor_system_resources(self):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        return {"cpu": cpu_percent, "memory": memory_percent}
