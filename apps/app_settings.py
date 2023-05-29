from zanos import Program
from power import Battery, PowerSupply
import time


class App_Settings(Program):
    def __init__(self, screen, d):
        super().__init__(screen)
        self.title = 'Settings'
        self.title_cn = b'\xc9\xe8\xd6\xc3'  # 设置
        # 齿轮
        self.icon = [0, 7, 224, 0, 0, 15, 240, 0, 0, 12, 48, 0, 3, 216, 27, 192, 7, 248, 31, 224, 14, 112, 14, 112, 28, 0, 0, 56, 24, 0, 0, 24, 24, 0, 0, 24, 28, 0, 0, 56, 12, 3, 192, 48, 28, 15, 240, 56, 120, 28, 56, 30, 224, 24, 24, 7, 192, 48, 12, 3, 192, 48,
                     12, 3, 192, 48, 12, 3, 192, 48, 12, 3, 192, 24, 24, 3, 120, 28, 56, 30, 28, 15, 240, 56, 12, 3, 192, 48, 28, 0, 0, 56, 24, 0, 0, 24, 24, 0, 0, 24, 28, 0, 0, 56, 14, 112, 14, 112, 7, 248, 31, 224, 3, 216, 27, 192, 0, 12, 48, 0, 0, 15, 240, 0, 0, 7, 224, 0]
        self.page = [
            'Set Language:',
            b'\xbc\xf2\xcc\xe5\xd6\xd0\xce\xc4',
            'English',
            b'\xa4\xcb\xa4\xdb\xa4\xf3\xa4\xb4',
        ]
        self.select_index = 1

    def run(self):
        self.screen.set_page(
        self.page, index=0, reverse_white_row=self.select_index)
        self.screen.set_reverse_white(True)
        self.screen.update_reverse_white_row(self.select_index)

    def handle(self, event):
        if event.signal in ['[LEFT]', '[UP]']:
            self.screen.roll_up()
            if self.select_index == 1:
                return
            self.select_index = self.select_index - 1
        elif event.signal in ['[RIGHT]', '[DOWN]']:
            self.screen.roll_down()
            if self.select_index == 3:
                return
            self.select_index = self.select_index + 1

    def quit(self):
        self.screen.set_reverse_white(False)
