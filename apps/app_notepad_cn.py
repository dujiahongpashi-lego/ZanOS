from zanos import Program
from screen import Screen
from article import Article
from pinyin_input import Pinyin_Input
from apps.remote_addr import get_addr
from uart import UART_PORT
import binascii


class App_Notepad_CN(Program):
    def __init__(self, screen: Screen, device: UART_PORT):
        super().__init__(screen, device)
        self.title = ' ChatGPT'
        self.title_cn = ' ChatGPT'  # b'\xd0\xb4\xd7\xd6\xb1\xbe' # 写字本
        self.icon = [0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 63, 192, 0, 0, 96, 127, 0, 0, 192, 97, 192, 0, 129, 128, 96, 1, 135, 0, 32, 1, 140, 8, 48, 7, 24, 62, 16, 13, 24, 99, 144, 25, 25, 192, 240, 17, 31, 112, 48, 49,
                     28, 24, 24, 33, 24, 14, 12, 33, 152, 15, 132, 48, 152, 8, 134, 16, 120, 8, 198, 24, 56, 8, 198, 12, 12, 56, 68, 7, 3, 248, 68, 7, 131, 136, 72, 4, 103, 8, 120, 4, 60, 8, 224, 4, 0, 48, 192, 2, 0, 96, 128, 3, 1, 128, 128, 1, 255, 1, 0, 0, 127, 7, 0, 0, 0, 252, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.input = Pinyin_Input()
        self.question = b''
        device.add_listener('HTTP_RESPONSE', self.show_answer)

    def show_answer(self, data):
        label = data['label']
        if label == 'chatgpt':
            resp = data['response']['data']
            gbk_bytes = binascii.unhexlify(resp)
            a = Article()
            a.reset_article_by_long_bytes(gbk_bytes)
            self.screen.show_article_slowly(a)
            self.question = b''

    def run(self):
        self.screen.set_reverse_white(False)
        self.screen.set_page([b'', '', '', ''])
        self.input.reset()
        self.screen.cursor_off()
        self.question = b''

    def handle(self, event):
        sig = event.signal
        reslut_str = self.input.input(sig)
        pinyin_str = self.input.get_pinyin()
        word = b''
        if sig == ' ':  # 选第一个
            if reslut_str:
                word = self.input.get_selected_word(0)
            else:
                word = b' '
        elif sig in ['1', '2', '3', '4']:  # 选第n个
            if reslut_str:
                word = self.input.get_selected_word(int(sig)-1)
            else:
                word = sig.encode()
        elif sig in ['?', ',', '.']:  # 符号直接输入
            word = {
                '?': b'\xa3\xbf',
                ',': b'\xa3\xac',
                '.': b'\xa1\xa3'
            }[sig]
        elif len(sig) == 1 and sig.isupper():  # 大写字母直接输入
            word = sig.encode()

        if word:
            self.input.reset()
            pinyin_str = self.input.get_pinyin()
            reslut_str = self.input.get_result()
            self.question += word
            line = self.question + b'_'
            self.screen.show_upper_two_lines(line)

        if sig == '[BACKSPACE]' and pinyin_str == '':
            self.question = self.question[:-2]
            line = self.question + b'_'
            self.screen.show_upper_two_lines(line)
        if sig == '[ENTER]':
            print(self.question)
            data = {
                'label': 'chatgpt',
                'url': 'http://' + get_addr()+'/?api=chatgpt&data=' + str(self.question)
            }
            self.device.send('REQ_HTTP', data)
            self.input.reset()
            pinyin_str = self.input.get_pinyin()
            reslut_str = self.input.get_result()

        self.screen.set_line(2, pinyin_str[0:16])
        self.screen.set_line(3, reslut_str[0:16])

    def quit(self):
        self.screen.cursor_off()
