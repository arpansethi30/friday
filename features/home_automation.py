import requests

class HomeAutomation:
    def __init__(self):
        self.devices = {}
        self.hub_url = "http://localhost:8080"  # Replace with actual hub URL

    def discover_devices(self):
        try:
            response = requests.get(f"{self.hub_url}/devices")
            self.devices = response.json()
            return True
        except:
            return False

    def control_device(self, device_id, command):
        if device_id in self.devices:
            try:
                response = requests.post(f"{self.hub_url}/device/{device_id}", json={"command": command})
                return response.status_code == 200
            except:
                return False
        return False

    def get_device_status(self, device_id):
        if device_id in self.devices:
            try:
                response = requests.get(f"{self.hub_url}/device/{device_id}/status")
                return response.json()
            except:
                return None
        return None
