from zanos import Program
from uart import UART_PORT


class App_Stock(Program):
    def __init__(self, screen, device: UART_PORT):
        super().__init__(screen)
        self.title = 'Stock Market'
        self.title_cn = b'\xc9\xcf\xd6\xa4\xd6\xb8\xca\xfd'  # 上证指数
        self.icon = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 253, 255, 255, 255, 241, 255, 255, 255, 193, 255, 255, 255, 129, 255, 255, 254, 1, 255, 255, 248, 1, 255, 255, 240, 1, 255, 255, 224, 1, 255, 255,
                     194, 17, 255, 191, 238, 49, 255, 31, 252, 49, 254, 31, 252, 113, 254, 15, 248, 113, 252, 15, 240, 255, 252, 15, 241, 255, 248, 71, 225, 255, 248, 199, 195, 255, 240, 195, 199, 255, 241, 227, 135, 255, 227, 225, 15, 255, 195, 241, 31, 255, 199, 240, 31, 255, 135, 240, 63, 255, 143, 248, 127, 255, 207, 248, 127, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        self.device = device
        self.screen = screen
        device.add_listener('HTTP_RESPONSE', self.show_stock)

    def show_stock(self, data):
        label = data['label']
        if label == 'stock':
            resp = data['response']
            print(resp)
            self.screen.set_line(1, 'SSE Index: ' +
                                 str(resp['Data'][0]['Latest']).split('.')[0])

    def run(self):
        data = {
            'label': 'stock',
            'url': 'http://api.gugudata.com/stock/cn/realtimeindex/demo'
        }
        self.device.send('REQ_HTTP', data)

    def handle(self, event):
        pass

    def quit(self):
        pass
