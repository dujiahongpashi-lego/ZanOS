from zanos import Program
from uart import UART_PORT
import random


class App_TestServer(Program):
    def __init__(self, screen, device: UART_PORT):
        super().__init__(screen)
        self.title = 'Test Server'
        self.title_cn = b'\xb7\xfe\xce\xf1\xbc\xe0\xb2\xe2' # 服务监测
        self.icon = [255, 255, 255, 255, 254, 0, 0, 31, 252, 0, 0, 15, 248, 255, 255, 199, 241, 255, 255, 231, 243, 255, 255, 243, 207, 255, 255, 243, 207, 255, 255, 243, 243, 255, 255, 243, 243, 255, 255, 243, 243, 128, 0, 115, 243, 128, 0, 115, 207, 255, 255, 243, 207, 255, 255, 243, 243, 128, 0, 115, 243, 128, 0,
                     115, 243, 255, 255, 243, 243, 255, 255, 243, 207, 128, 0, 115, 207, 128, 0, 115, 243, 255, 255, 243, 243, 255, 255, 243, 243, 128, 0, 115, 243, 128, 0, 115, 207, 255, 255, 243, 207, 255, 255, 243, 243, 255, 255, 243, 241, 255, 255, 231, 248, 255, 255, 199, 252, 0, 0, 15, 254, 0, 0, 31, 255, 255, 255, 255]
        self.device = device
        self.screen = screen
        device.add_listener('HTTP_RESPONSE', self.show_resp)

    def show_resp(self, data):
        label = data['label']
        if label == 'testServer':
            resp = data['response']
            self.screen.set_line(2 , resp)

    def run(self):
        send_data = random.randint(0,100)
        self.screen.set_line(1 , str(send_data))
        data = {
            'label':'testServer',
            'url':'https://localhost:3000/api=encode&data=LEGO' + str(send_data)
        }
        self.device.send('REQ_HTTP', data)

    def handle(self, event):
        pass

    def quit(self):
        pass
