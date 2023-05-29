from zanos import Program
from uart import UART_PORT


class App_Bilibili(Program):
    def __init__(self, screen, device: UART_PORT):
        super().__init__(screen)
        self.title = ' B-Index'
        self.title_cn = b' B\xca\xfd\xcf\xd4\xca\xbe'  # B数显示
        self.icon = [0, 192, 1, 128, 1, 224, 3, 192, 0, 240, 7, 128, 0, 120, 15, 0, 0, 60, 30, 0, 15, 255, 255, 240, 63, 255, 255, 252, 127, 255, 255, 254, 248, 0, 0, 31, 224, 0, 0, 7, 224, 0, 0, 7, 224, 24, 24, 7, 224, 252, 63, 7, 227, 252, 63, 199, 231, 224, 7, 231, 227, 0, 0, 199, 224, 0, 0, 7, 224, 0, 0, 7, 224, 0, 0, 7, 224, 0, 128, 7, 224, 25, 204, 7, 224, 31, 124, 7, 224, 14, 56, 7, 224, 0, 0, 7, 224, 0, 0, 7, 248,
                     0, 0, 31, 127, 255, 255, 254, 63, 255, 255, 252, 15, 255, 255, 240, 1, 224, 7, 128, 0, 0, 0, 0, 0, 0, 0, 0]
        self.device = device
        self.screen = screen
        device.add_listener('HTTP_RESPONSE', self.show_fans)

    def show_fans(self, data):
        label = data['label']
        if label == 'bilifans':
            resp = data['response']
            self.screen.set_line(
                1, 'B-Index: ' + str(resp['data']['follower']))

    def run(self):
        data = {
            'label': 'bilifans',
            'url': 'http://api.bilibili.com/x/relation/stat?vmid=242649949'
        }
        self.device.send('REQ_HTTP', data)

    def handle(self, event):
        pass

    def quit(self):
        pass
