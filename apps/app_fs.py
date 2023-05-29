from zanos import Program, EVENT_TYPE
from filesystem import FS
from article import Article


class App_FS(Program):
    def __init__(self, screen, d):
        super().__init__(screen)
        self.title = 'File System'
        self.title_cn = b'\xce\xc4\xbc\xfe\xcf\xb5\xcd\xb3' # 文件系统
        self.icon = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 192, 7, 255, 255, 191, 251, 255, 255, 191, 251, 255, 255, 191, 251, 255, 255, 191, 248, 0,
                     63, 191, 255, 255, 191, 191, 255, 255, 191, 191, 255, 255, 191, 191, 255, 255, 191, 188, 0, 0, 1, 189, 255, 255, 253, 189, 255, 255, 253, 185, 255, 255, 253, 187, 255, 255, 249, 179, 255, 255, 251, 183, 255, 255, 243, 183, 255, 255, 247, 167, 255, 255, 247, 175, 255, 255, 231, 175, 255, 255, 239, 143, 255, 255, 207, 159, 255, 255, 223, 159, 255, 255, 223, 128, 0, 0, 31, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        self.current_files = []
        self.select_index = 0
        self.fs = FS()
        self.mode = 'list'
        self.article = Article()

    def get_show_names(self, files):
        list = []
        for f in files:
            list.append(f['show_name'])
        return list

    def show_list(self):
        # page = [self.fs.get_current_folder_show_name()] + \
        #    self.get_show_names(self.current_files)
        page = self.get_show_names(self.current_files)
        self.screen.set_page(
            page, index=self.select_index, reverse_white_row=0)
        self.screen.set_reverse_white(True)
        self.screen.update_reverse_white_row(self.select_index)

    def run(self):
        self.screen.icon_clean(7, 0)
        self.current_files = self.fs.get_files()
        self.show_list()

    def into_file(self, file):
        self.mode = 'file'
        lines = self.fs.open(file['name'])
        self.article.set_article(lines)
        self.screen.show_article(self.article)
        self.screen.set_reverse_white(False)
        self.screen.cursor_off()

    def into_folder(self, file):
        self.fs.goto_dir(file['name'])
        self.current_files = self.fs.get_files()
        self.select_index = 0
        self.show_list()

    def quit_file(self):
        self.screen.cursor_off()
        file = self.current_files[self.select_index]
        self.fs.save(file['name'], self.article.lines)
        self.mode = 'list'
        self.select_index = 0
        self.show_list()

    def quit_folder(self):
        self.fs.goto_dir('..')
        self.current_files = self.fs.get_files()
        self.show_list()

    def edit_file(self, event):
        self.article.handle_move_signal(event.signal)
        self.article.handle_del_signal(event.signal)
        if event.evt_type == EVENT_TYPE.CHAR_INPUT:
            self.article.handle_input(event.signal)
        self.screen.show_article(self.article)

    def select_file(self, event):
        if event.signal in ['[LEFT]', '[UP]']:
            self.screen.roll_up()
            if self.select_index == 0:
                return
            self.select_index = self.select_index - 1
        elif event.signal in ['[RIGHT]', '[DOWN]']:
            self.screen.roll_down()
            if self.select_index == len(self.current_files) - 1:
                return
            self.select_index = self.select_index + 1

    def handle(self,  event):
        if self.mode == 'list':
            self.select_file(event)
            file = self.current_files[self.select_index]
            print(file['name'])
            if event.signal in ['[BACKSPACE]', '[CTRL]']:
                self.quit_folder()
            if file['type'] == 'FOLDER' and event.signal == '[ENTER]':
                self.into_folder(file)
            if file['type'] == 'FILE' and event.signal == '[ENTER]':
                self.into_file(file)
        elif self.mode == 'file':
            if event.signal in ['[ENTER]', '[CTRL]']:
                self.quit_file()
                return
            self.edit_file(event)

    def quit(self):
        self.screen.set_reverse_white(False)
        self.screen.cursor_off()
        return super().quit()
