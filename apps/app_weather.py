from zanos import Program
from uart import UART_PORT


class App_Weather(Program):
    def __init__(self, screen, device: UART_PORT):
        super().__init__(screen)
        self.title = 'Weather'
        self.title_cn = b'\xbc\xc3\xc4\xcf\xcc\xec\xc6\xf8'  # 济南天气
        self.icon = [63, 255, 255, 252, 127, 255, 255, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255, 224, 63, 255, 255, 192, 31, 255, 255, 128, 7, 255, 255, 128, 3, 255, 255, 0, 1, 255, 254, 0, 0, 255, 248, 0, 0, 63, 240, 0, 0, 31, 224, 0, 0, 15, 224, 0, 0, 15, 224, 0, 0, 7, 224, 0, 0, 7, 224, 0, 0, 15, 240, 0, 0, 31, 252, 0, 0, 63, 255, 255, 255, 255, 255, 223, 255, 255, 255, 142, 115, 255, 255, 156, 227, 255, 255, 248, 231, 255, 255, 249, 199, 255, 255, 255, 143, 255, 255, 255, 159, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127, 255, 255, 254, 63, 255, 255, 252]
        self.device = device
        self.screen = screen
        device.add_listener('HTTP_RESPONSE', self.show_weather)

    def show_weather(self, data):
        label = data['label']
        if label == 'weather':
            resp = data['response']
            self.screen.set_line(0, ('JiNan '+ str(resp['results'][0]['now']['temperature'])).encode() + b'\xa1\xe6')
            self.screen.set_line(1, 'Weather: Cloudy')

    def run(self):
        data = {
            'label': 'weather',
            'url': 'http://api.seniverse.com/v3/weather/now.json?key=Ssgu9E0JLMgna-pzm&location=jinan' # 为防滥用，已将此key注销了
        }
        self.device.send('REQ_HTTP', data)

    def handle(self, event):
        pass

    def quit(self):
        pass
