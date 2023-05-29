import network
import urequests
import json


class WifiNetwork:
    def __init__(self) -> None:
        self.ssid = ''
        self.station = None

    def connect(self, ssid, password):
        self.station = network.WLAN(network.STA_IF)
        if self.is_connected():
            return
        self.station.active(True)
        self.station.connect(ssid, password)
        self.ssid = ssid

    def is_connected(self):
        if not self.station:
            return False
        return self.station.isconnected()

    def get_request(self, url, cb):
        response = urequests.get(url)
        # By chatGPT
        if response.status_code == 200:
            payload = response.text
            print("HTTP GET", payload)
            data = json.loads(payload)
            cb(data)
            return True
        else:
            print("HTTP GET请求失败")
            return False
