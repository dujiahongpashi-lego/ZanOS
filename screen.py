from lcd12864 import LCD
from oled12864 import OLED
from article import Article
import time


class Screen:
    def __init__(self, lcd: LCD, oled: OLED = None, page=['', '', '', ''], index=0):
        lcd.draw_clean()
        self.lcd = lcd
        self.oled = oled
        self.lines = ['', '', '', '']
        self.page = page
        self.row_no = index
        self.cursor_off()
        self._refresh_screen()
        self.reverse_white_on = True  # 开启按行反白
        self.reverse_white_row = 0
        # self._refresh_reverse_white(0, 0)

    def _refresh_reverse_white(self, pre, nxt):
        self.lcd.draw_row_underline(pre, 'clean')
        if not self.reverse_white_on:
            return
        line = self.lines[nxt]
        length = len(line) / 2
        if length > 8:
            length = 8
        self.lcd.draw_row_underline(nxt, 'fill', length)

    def _refresh_screen(self):  # 1 3 2 4 顺序依次写入
        for row in [0, 2, 1, 3]:
            self._update_line(row, self.page[self.row_no + row])

    def _update_line(self, no, new_line, start=0):
        old_line = self.lines[no]
        line = self.lines[no] = new_line
        if type(old_line) != type(line) or not old_line in new_line:  # 非追加或不变
            self.lcd.display_str(no, 0, '                ')

        if type(line) is bytes:
            self.lcd.display_encode_str(no, start, line)
        else:
            self.lcd.display_str(no, start, line)

    def set_page(self, page, index=-1, reverse_white_row=-1):
        if index == -1:
            index = self.row_no
        if reverse_white_row == -1:
            reverse_white_row = self.reverse_white_row
        self.page = page + [''] * (4 - len(page))
        self.row_no = index
        if self.reverse_white_on:
            self._refresh_reverse_white(
                self.reverse_white_row, reverse_white_row)
        self.reverse_white_row = reverse_white_row
        self._refresh_screen()

    def set_line(self, no, line, centered=False):
        start = 0
        if centered:
            start = (16 - len(line)) // 4

        self._update_line(no, line, start)

    def append_to_line(self, no, str):
        self._update_line(no, self.lines[no] + str)

    def update_reverse_white_row(self, no):
        self.reverse_white_row = no
        self._refresh_reverse_white(no, no)

    def set_reverse_white(self, enable=True):
        self.reverse_white_on = enable
        self._refresh_reverse_white(
            self.reverse_white_row, self.reverse_white_row)

    # 光标关
    def cursor_off(self):
        self.lcd.cursor_off()

    # 光标开
    def cursor_on(self, is_block_cursor = False):
        self.lcd.cursor_on(is_block_cursor)

    def roll_down(self):
        if self.reverse_white_on and self.reverse_white_row < 3:
            pre = self.reverse_white_row
            nxt = self.reverse_white_row + 1
            self.reverse_white_row = nxt
            self._refresh_reverse_white(pre, nxt)
        elif self.row_no + 4 < len(self.page):
            self.row_no += 1
            self._refresh_screen()
            if self.reverse_white_on:
                self._refresh_reverse_white(
                    self.reverse_white_row, self.reverse_white_row)

    def roll_up(self):
        if self.reverse_white_on and self.reverse_white_row > 0:
            pre = self.reverse_white_row
            nxt = self.reverse_white_row - 1
            self.reverse_white_row = nxt
            self._refresh_reverse_white(pre, nxt)
        elif self.row_no > 0:
            self.row_no -= 1
            self._refresh_screen()
            if self.reverse_white_on:
                self._refresh_reverse_white(
                    self.reverse_white_row, self.reverse_white_row)

    def set_status_bar(self):
        self.lcd.enable_icon_wifi(0, 0)
        self.lcd.enable_icon_battery(7, 0)

    def show_img(self, img, img_type='center64', x=0, y=0):
        if img_type == 'center64':
            self.lcd.draw_img_small(img)
        elif img_type == '32':
            self.lcd.draw_img_32(x, y, img)
            self.oled.draw_img_32(x, y, img)
        elif img_type == 'blank32':
            self.lcd.draw_img_32(x, y, None)

    def draw_clean(self):
        self.lcd.draw_clean()

    def show_icon(self, icon_type='wifi', x=0, y=0):
        if icon_type == 'wifi':
            self.lcd.enable_icon_wifi(x, y)
        elif icon_type == 'battery':
            self.lcd.enable_icon_battery(x, y)
        elif icon_type == 'battery_i':
            self.lcd.enable_icon_battery_incharge(x, y)

    def icon_clean(self, x, y):
        self.lcd.clean_icon(x, y)

    def show_article(self, article: Article):
        i = article.line_index
        page = article.lines[i:][:4] + [''] * (4 - len(article.lines[i:][:4]))
        self.set_page(page, index=0)
        self.cursor_to(article.cursor_x, article.cursor_y)
    
    def cursor_to(self, cursor_x, cursor_y, mode = False):
        self.lcd.cursor_to(cursor_x, cursor_y, mode)

    def show_article_slowly(self, article: Article):
        for i in range(len(article.lines)):
            line = article.lines[i]
            self.show_line_slowly(3, line)
            if i < len(article.lines) - 1 and line:
                self.set_page([
                    self.lines[1],
                    self.lines[2],
                    self.lines[3],
                    ''
                ], index=0)

    def show_line_slowly(self, no, line):
        if type(line) is not bytes or not line:
            return

        start = 0
        while start < len(line):
            stop = start + 2  # 每次两个字节 by chatgpt
            self.set_line(no, line[0:stop])
            start = stop
            time.sleep_ms(200)

    def show_upper_two_lines(self, long_bytes):
        print(long_bytes, len(long_bytes))
        m = len(long_bytes)  # 获取字符串长度
        n = m % 16  # 模除16余数 n
        if m <= 16:
            self.set_line(0, long_bytes[-n:])
            self.set_line(1, '                ')
        else:
            self.set_line(0, long_bytes[-n-16: -n])
            self.set_line(1, long_bytes[-n:])

    def debug(self, msg_title='', msg_body=''):
        if not msg_title and not msg_body:
            self.set_line(1, '                ')
            self.set_line(2, '                ')
        else:
            self.set_line(1, msg_title)
            self.set_line(2, msg_body)
