from zanos import Program
from uart import UART_PORT


class App_Test_CN(Program):
    def __init__(self, screen, device: UART_PORT):
        super().__init__(screen)
        self.title = 'Test Chinese'
        self.title_cn = 'Test Chinese'
        self.icon = [63, 254, 127, 252, 127, 252, 63, 254, 255, 252, 63, 255, 255, 252, 63, 255, 255, 252, 63, 255, 255, 248, 31, 255, 255, 248, 31, 255, 255, 248, 31, 255, 255, 240, 15, 255, 255, 241, 143, 255, 255, 241, 143, 255, 255, 225, 135, 255, 255, 3, 192, 255, 248, 3, 192, 31, 192, 15, 240, 3, 128, 127, 254, 1, 128, 127, 254, 1, 192, 15, 240, 3, 248, 3, 192, 31, 255, 3, 192, 255, 255, 225, 135, 255, 255, 241, 143, 255, 255, 241, 143, 255, 255, 240, 143, 255, 255, 248, 31, 255, 255, 248, 31, 255, 255, 248, 31, 255, 255, 252, 63, 255, 255, 252, 63, 255, 255, 252, 63, 255, 127, 252, 63, 254, 63, 254, 127, 252]
        self.screen = screen

    def run(self):
        self.screen.set_line(1, b'\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef')
        self.screen.set_line(2, b'\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xef\xbf')
        self.screen.set_line(3, b'\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xef\xbf\xbd\xef')
        self.screen.set_line(0, b'\x02\x02\x02\x02\x02\x02\x02')

    def handle(self, event):
        pass

    def quit(self):
        pass
