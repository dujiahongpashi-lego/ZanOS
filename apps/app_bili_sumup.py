from zanos import Program, EVENT_TYPE
from uart import UART_PORT
from article import Article
from apps.remote_addr import get_addr
import binascii


class App_BiliSumup(Program):
    def __init__(self, screen, device: UART_PORT):
        super().__init__(screen)
        self.title = 'Bili Sumup'
        self.title_cn = b'\xca\xa1\xc1\xf7\xc9\xf1\xc6\xf7'  # 省流神器
        self.icon = [0, 192, 1, 128, 1, 224, 3, 192, 0, 240, 7, 128, 0, 120, 15, 0, 0, 60, 30, 0, 15, 255, 255, 240, 63, 255, 255, 252, 127, 255, 255, 254, 248, 0, 0, 31, 224, 16, 0, 7, 224, 24, 0, 7, 224, 30, 0, 7, 224, 31, 128, 7, 224, 31, 192, 7, 224, 31, 240, 7, 224, 31,
                     252, 7, 224, 31, 254, 7, 224, 31, 252, 7, 224, 31, 240, 7, 224, 31, 192, 7, 224, 31, 128, 7, 224, 30, 0, 7, 224, 24, 0, 7, 224, 16, 0, 7, 224, 0, 0, 7, 248, 0, 0, 31, 127, 255, 255, 254, 63, 255, 255, 252, 15, 255, 255, 240, 1, 192, 3, 128, 0, 0, 0, 0, 0, 0, 0, 0]
        self.device = device
        self.screen = screen
        self.article = Article()
        device.add_listener('HTTP_RESPONSE', self.show_artcicle)

    def show_artcicle(self, data):
        label = data['label']
        if label == 'bilisumup':
            resp = data['response']['data']
            gbk_bytes = binascii.unhexlify(resp)
            self.article.reset_article_by_long_bytes(gbk_bytes)
            self.screen.show_article_slowly(self.article)

    def run(self):
        self.screen.set_reverse_white(False)
        self.article.reset()
        self.article.set_article(
            [b'\xc7\xeb\xca\xe4\xc8\xebBV', '', '', ''])  # 请输入BV
        self.article.move_cursor('down')
        self.screen.show_article(self.article)
        self.screen.cursor_on()

        # bs = b'\xce\xd2\xb5\xc4\xcc\xec\xbf\xd5\xa3\xac\xbd\xf1\xcc\xec\xd3\xd0\xb5\xe3\xbb\xd2\xa1\xa3\n\xce\xd2\xb5\xc4\xd0\xc4\xa3\xac\xca\xc7\xb8\xf6\xc2\xe4\xd2\xb6\xb5\xc4\xbc\xbe\xbd\xda\xa1\xa3\n\xce\xd2\xb2\xbb\xd6\xaa\xb5\xc0\xc8\xe7\xba\xce\xb6\xc8\xb9\xfd\xbd\xf1\xd2\xb9\xa3\xac\n\xcb\xf9\xd3\xd0\xb5\xc4\xb5\xc6\xb6\xbc\xd2\xd1\xbe\xad\xc8\xab\xb2\xbf\xcf\xa8\xc3\xf0\xa1\xa3'
        # self.article.reset_article_by_long_bytes(bs)
        # self.screen.show_article_slowly(self.article)

    def handle(self, event):
        self.article.handle_move_signal(event.signal)
        self.article.handle_del_signal(event.signal)
        if event.evt_type == EVENT_TYPE.CHAR_INPUT:
            self.article.handle_input(event.signal)
        elif event.signal == '[F9]': # 快速输入
            self.article.set_article(
            [b'\xc7\xeb\xca\xe4\xc8\xebBV', 'BV1cy4y1k7A2', '', ''])
        elif event.signal == '[ENTER]':
            bvid = self.article.get_line(1)
            if type(bvid) is not str:
                print(bvid, 'not str')
                return
            data = {
                'label': 'bilisumup',
                'url': 'http://' + get_addr()+'/?api=bilisumup&data=' + bvid
            }
            self.device.send('REQ_HTTP', data)

        self.screen.show_article(self.article)

    def quit(self):
        self.screen.cursor_off()
