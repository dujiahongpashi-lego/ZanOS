class Article:
    def __init__(self, lines=['','','',''], height=4, width=8) -> None:
        self.lines = lines
        self.height = height
        self.width = width
        self.reset()

    def reset(self):
        self.line_index = 0
        self.cursor_x = 0
        self.cursor_y = 0

    def get_line(self, n):
        if len(self.lines) < n + 1:
            return ''
        return self.lines[n]

    def set_article(self, lines):
        self.lines = lines + [''] * (4 - len(lines)) # 至少4行
        self.reset()

    def reset_article_by_long_bytes(self, long_bytes):  # by chatgpt
        lines = []
        i = 0
        while i < len(long_bytes):
            line_bytes = long_bytes[i:i+16]
            idx_n = line_bytes.find(b'\n')
            if idx_n != -1:
                line_bytes = line_bytes.split(b'\n')[0]
                i += idx_n + 1
            else:
                i += 16
            lines.append(line_bytes)
        self.reset()
        self.set_article(lines)

    def handle_del_signal(self, signal):
        if signal == '[BACKSPACE]':
            y = self.cursor_y + self.line_index
            line = self.lines[y][:-1]
            self.cursor_x = len(line) // 2
            self.lines[y] = line

    def handle_input(self, signal):
        y = self.cursor_y + self.line_index
        print(self.cursor_y, len(self.lines), self.line_index)
        if len(self.lines[y]) >= 2 * self.width:
            return
        line = self.lines[y] + signal
        x = len(line) // 2
        if x >= self.width:
            x = self.width - 1
        self.cursor_x = x
        self.lines[y] = line

    def handle_move_signal(self, signal):
        if signal == '[LEFT]':
            self.move_cursor('left')
        elif signal == '[RIGHT]':
            self.move_cursor('right')
        elif signal == '[UP]':
            self.move_cursor('up')
        elif signal == '[DOWN]':
            self.move_cursor('down')

    def move_cursor(self, dir='down'):
        if dir == 'down':
            if self.cursor_y >= self.height - 1:
                if self.line_index < len(self.lines) - self.height:
                    self.line_index += 1
            else:
                self.cursor_y += 1
        if dir == 'up':
            if self.cursor_y <= 0:
                if self.line_index > 0:
                    self.line_index -= 1
            else:
                self.cursor_y -= 1
        if dir == 'left' and self.cursor_x > 0:
            self.cursor_x -= 1
        if dir == 'right' and self.cursor_x < self.width - 1:
            self.cursor_x += 1

    def edit_line(self, n, new_line):
        self.lines[n] = new_line
