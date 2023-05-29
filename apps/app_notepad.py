from zanos import Program, EVENT_TYPE
from screen import Screen
from filesystem import FS
from article import Article


class App_Notepad(Program):
    def __init__(self, screen: Screen, d):
        super().__init__(screen)
        self.title = 'Notepad'
        self.title_cn = b'  \xb1\xb8\xcd\xfc\xc2\xbc' # 备忘录
        self.icon = [63, 255, 255, 252, 126, 0, 0, 30, 252, 0, 0, 15, 248, 255, 255, 199, 241, 255, 255, 231, 243, 255, 255, 243, 207, 255, 255, 243, 207, 255, 255, 243, 243, 255, 255, 243, 243, 255, 255, 243, 243, 128, 0, 115, 243, 128, 0, 115, 207, 255, 255, 243, 207, 255, 255, 243, 243, 128, 0, 115, 243, 128, 0, 115, 243, 255, 255, 243, 243, 255, 255, 243, 207, 128, 0, 115, 207, 128, 0, 115, 243, 255, 255, 243, 243, 255, 255, 243, 243, 128, 0, 115, 243, 128, 0, 115, 207, 255, 255, 243, 207, 255, 255, 243, 243, 255, 255, 243, 241, 255, 255, 231, 248, 255, 255, 199, 252, 0, 0, 15, 126, 0, 0, 30, 63, 255, 255, 252]
        self.article = Article()

    def run(self):
        lines = FS().open('apps/note.txt')
        self.screen.set_reverse_white(False)
        self.article.reset()
        self.article.set_article(lines)
        self.screen.show_article(self.article)
        self.screen.cursor_on()

    def handle(self, event):
        self.article.handle_move_signal(event.signal)
        self.article.handle_del_signal(event.signal)
        if event.evt_type == EVENT_TYPE.CHAR_INPUT:
            self.article.handle_input(event.signal)
        self.screen.show_article(self.article)

    def quit(self):
        self.screen.cursor_off()
        FS().save('apps/note.txt', self.article.lines)
