from zanos import Program, EVENT_TYPE
from screen import Screen
from filesystem import FS
from article import Article


class App_Game(Program):
    def __init__(self, screen: Screen, d):
        super().__init__(screen)
        self.title = 'Game'
        self.title_cn = b'\xd0\xc7\xf1\xb7\xcc\xfa\xb5\xc0' # 星穹铁道
        self.icon = [63, 255, 255, 252, 126, 0, 0, 30, 252, 0, 0, 15, 248, 255, 255, 199, 241, 255, 255, 231, 243, 255, 255, 243, 207, 255, 255, 243, 207, 255, 255, 243, 243, 255, 255, 243, 243, 255, 255, 243, 243, 128, 0, 115, 243, 128, 0, 115, 207, 255, 255, 243, 207, 255, 255, 243, 243, 128, 0, 115, 243, 128, 0, 115, 243, 255, 255, 243, 243, 255, 255, 243, 207, 128, 0, 115, 207, 128, 0, 115, 243, 255, 255, 243, 243, 255, 255, 243, 243, 128, 0, 115, 243, 128, 0, 115, 207, 255, 255, 243, 207, 255, 255, 243, 243, 255, 255, 243, 241, 255, 255, 231, 248, 255, 255, 199, 252, 0, 0, 15, 126, 0, 0, 30, 63, 255, 255, 252]
        self.cursor_x = 0
        self.cursor_y = 0

    def run(self):
        self.screen.cursor_on(True)

    def handle(self, event):
        self.handle_move_signal(event.signal)
        self.screen.cursor_to(self.cursor_x, self.cursor_y, True)

    def handle_move_signal(self, signal):
        if signal == 'a' :
            self.move_cursor('left')
        elif signal == 'd':
            self.move_cursor('right')
        elif signal == 'w':
            self.move_cursor('up')
        elif signal == 's':
            self.move_cursor('down')

    def move_cursor(self, dir='down'):
        if dir == 'down' and self.cursor_y < 3:
            self.cursor_y += 1
        if dir == 'up' and self.cursor_y > 0:
            self.cursor_y -= 1
        if dir == 'left' and self.cursor_x > 0:
            self.cursor_x -= 1
        if dir == 'right' and self.cursor_x < 8:
            self.cursor_x += 1

    def quit(self):
        self.screen.cursor_off()
