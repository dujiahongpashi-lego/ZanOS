from zanos import Program
from power import Battery, PowerSupply
import time


class App_Shutdown(Program):
    def __init__(self, screen, d):
        super().__init__(screen)
        self.title = 'Settings'
        self.title = 'shutdown'
        self.title_cn = b'\xc9\xe8\xd6\xc3'  # 设置
        self.title_cn = b'\xb9\xd8\xbb\xfa' # 关机
        # 齿轮
        self.icon = [0, 7, 224, 0, 0, 15, 240, 0, 0, 12, 48, 0, 3, 216, 27, 192, 7, 248, 31, 224, 14, 112, 14, 112, 28, 0, 0, 56, 24, 0, 0, 24, 24, 0, 0, 24, 28, 0, 0, 56, 12, 3, 192, 48, 28, 15, 240, 56, 120, 28, 56, 30, 224, 24, 24, 7, 192, 48, 12, 3, 192, 48,
                     12, 3, 192, 48, 12, 3, 192, 48, 12, 3, 192, 24, 24, 3, 120, 28, 56, 30, 28, 15, 240, 56, 12, 3, 192, 48, 28, 0, 0, 56, 24, 0, 0, 24, 24, 0, 0, 24, 28, 0, 0, 56, 14, 112, 14, 112, 7, 248, 31, 224, 3, 216, 27, 192, 0, 12, 48, 0, 0, 15, 240, 0, 0, 7, 224, 0]
        # 关机
        self.icon = [0, 1, 192, 0, 0, 3, 224, 0, 0, 3, 224, 0, 0, 3, 224, 0, 0, 3, 224, 0, 1, 227, 227, 192, 3, 227, 227, 224, 7, 227, 227, 240, 15, 227, 227, 248, 31, 195, 225, 252, 31, 131, 224, 252, 63, 3, 224, 126, 63, 3, 224, 126, 62, 3, 224, 62, 126, 3, 224, 63, 124, 3, 224, 31, 124, 3, 224, 31, 124, 1, 192, 31, 124, 0, 0, 31, 126, 0, 0, 63, 126, 0, 0, 63, 62, 0, 0, 62, 63, 0, 0, 126, 63, 128, 0, 254, 31, 192, 1, 252, 15, 224, 3, 248, 15, 240, 7, 248, 7, 255, 255, 240, 3, 255, 255, 224, 1, 255, 255, 192, 0, 127, 255, 0, 0, 31, 252, 0]
    def run(self):
        p = PowerSupply()
        p.disable_power_supply()
        time.sleep(5)
        p.enable_power_supply()
        # self.screen.set_line(0, b'F11 \xb9\xd8\xbb\xfa')  # 'F11 关机'
        # self.screen.set_line(
        #     1, b'F12 \xd6\xd8\xc6\xf4\xcb\xf9\xd3\xd0\xcd\xe2\xc9\xe8')  # 'F12 重启所有外设'

        self.screen.set_line(0, b'\xb9\xd8\xbb\xfa')  # '关机'
        self.screen.set_line(
            1, b'\xd6\xd8\xc6\xf4')  # '重启'

    def handle(self, event):
        if event.signal == '[F11]': # 切断电池供电
            Battery().disable_battery_power()
        elif event.signal == '[F12]':
            p = PowerSupply()
            p.disable_power_supply()
            time.sleep(1)
            p.enable_power_supply()

    def quit(self):
        pass
