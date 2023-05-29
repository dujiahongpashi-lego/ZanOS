from zanos import Program, EVENT_TYPE
from uart import UART_PORT
from article import Article
from apps.remote_addr import get_addr
import binascii


class App_BiliHot(Program):
    def __init__(self, screen, device: UART_PORT):
        super().__init__(screen)
        self.title = 'Bili Hot'
        self.title_cn = b' B\xd5\xbe\xc8\xc8\xc3\xc5\xca\xd3\xc6\xb5'  # B站热门视频
        self.icon = [0, 192, 1, 128, 1, 224, 3, 192, 0, 240, 7, 128, 0, 120, 15, 0, 0, 60, 30, 0, 15, 255, 255, 240, 63, 255, 255, 252, 127, 255, 255, 254, 248, 0, 0, 31, 224, 16, 0, 7, 224, 24, 0, 7, 224, 30, 0, 7, 224, 31, 128, 7, 224, 31, 192, 7, 224, 31, 240, 7, 224, 31,
                     252, 7, 224, 31, 254, 7, 224, 31, 252, 7, 224, 31, 240, 7, 224, 31, 192, 7, 224, 31, 128, 7, 224, 30, 0, 7, 224, 24, 0, 7, 224, 16, 0, 7, 224, 0, 0, 7, 248, 0, 0, 31, 127, 255, 255, 254, 63, 255, 255, 252, 15, 255, 255, 240, 1, 192, 3, 128, 0, 0, 0, 0, 0, 0, 0, 0]
        self.device = device
        self.screen = screen
        self.article = Article()
        self.current = None
        self.select_index = 0
        device.add_listener('HTTP_RESPONSE', self.show_http_resp)
        # device.add_listener('WIFI_STATUS', self.got_connect_status)

        # https://api.bilibili.com/x/web-interface/popular/precious 热门视频接口
        self.hot_bv = {
            # 【才浅】15天花20万元用500克黄金敲数万锤纯手工打造三星堆黄金面具
            b'\xa1\xbe\xb2\xc5\xc7\xb3\xa1\xbf15\xcc\xec\xbb\xa820\xcd\xf2\xd4\xaa\xd3\xc3500\xbf\xcb\xbb\xc6\xbd\xf0\xc7\xc3\xca\xfd\xcd\xf2\xb4\xb8\xb4\xbf\xca\xd6\xb9\xa4\xb4\xf2\xd4\xec\xc8\xfd\xd0\xc7\xb6\xd1\xbb\xc6\xbd\xf0\xc3\xe6\xbe\xdf': 'BV16X4y1g7wT',
            # 【何同学】80年代的电脑能做什么？苹果麦金塔深度体验
            b'\xa1\xbe\xba\xce\xcd\xac\xd1\xa7\xa1\xbf80\xc4\xea\xb4\xfa\xb5\xc4\xb5\xe7\xc4\xd4\xc4\xdc\xd7\xf6\xca\xb2\xc3\xb4\xa3\xbf\xc6\xbb\xb9\xfb\xc2\xf3\xbd\xf0\xcb\xfe\xc9\xee\xb6\xc8\xcc\xe5\xd1\xe9': 'BV1cy4y1k7A2',
            # 敢杀我的马？！
            b'  \xb8\xd2  \xc9\xb1  \xce\xd2  \xb5\xc4  \xc2\xed\xa3\xbf\xa3\xa1': 'BV1yt4y1Q7SS',
            # 《这才叫水视频！》创意短片
            b'\xa1\xb6\xd5\xe2\xb2\xc5\xbd\xd0\xcb\xae\xca\xd3\xc6\xb5\xa3\xa1\xa1\xb7\xb4\xb4\xd2\xe2\xb6\xcc\xc6\xac': 'BV1FE411A7Xd',
        }
        self.hot_list = list(self.hot_bv.keys())

        self.page = []
        for key in self.hot_list:
            self.page.append(key)

    # def got_connect_status(self, data):
    #     if data['status'] == 'online':
    #         return
    #     else:
    #         self.screen.set_line(0, 'WIFI lost')

    def show_http_resp(self, data):
        label = data['label']
        if label == 'bilisumup':
            self.screen.show_article(Article())  # clean
            resp = data['response']['data']
            gbk_bytes = binascii.unhexlify(resp)
            self.article.reset_article_by_long_bytes(gbk_bytes)
            self.screen.show_article_slowly(self.article)

    def run(self):
        self.select_index = 0
        self.screen.set_page(
            self.page, index=0, reverse_white_row=self.select_index)
        self.screen.set_reverse_white(True)
        self.screen.update_reverse_white_row(self.select_index)

    def handle(self, event):
        if event.signal in ['[LEFT]', '[UP]']:
            self.screen.roll_up()
            if self.select_index == 0:
                return
            self.select_index = self.select_index - 1
        elif event.signal in ['[RIGHT]', '[DOWN]']:
            self.screen.roll_down()
            if self.select_index == len(self.hot_list) - 1:
                return
            self.select_index = self.select_index + 1
        elif event.signal in ['[ENTER]']:
            self.screen.set_reverse_white(False)
            self.request_bv_sumup()

    def request_bv_sumup(self):
        title = self.hot_list[self.select_index]
        bvid = self.hot_bv[title]
        data = {
            'label': 'bilisumup',
            'url': 'http://' + get_addr()+'/?api=bilisumup&data=' + bvid
        }
        self.device.send('REQ_HTTP', data)

    def quit(self):
        self.screen.cursor_off()
        self.screen.set_reverse_white(False)
