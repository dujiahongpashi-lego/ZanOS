from zanos import Program
from screen import Screen
from uart import UART_PORT


class App_WIFI(Program):
    def __init__(self, screen: Screen, device: UART_PORT):
        self.title = 'WIFI'
        self.title_cn = 'WIFI'
        self.icon = [63, 255, 255, 252, 127, 255, 255, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 192, 3, 255, 252, 0, 0, 63, 224, 0, 0, 7, 128, 63, 252, 1, 3, 255, 255, 192, 159, 255, 255, 249, 255, 240, 7, 255, 255, 0, 0, 127, 248, 0, 0, 15, 248, 15, 248, 15, 252, 255, 255, 159, 255, 255, 255, 255, 255, 240, 7, 255, 255, 128, 0, 255, 255, 192, 1, 255, 255, 231, 243, 255, 255, 255, 255, 255, 255, 248, 15, 255, 255, 252, 31, 255, 255, 254, 63, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127, 255, 255, 254, 63, 255, 255, 252]
        
        self.wifi_list = {
            'SOHO': '********',
            'HOSO-SHUFANG': '********',
            'HOSO': '********',
            'STORE_JIA': '********',
            'STORE_LAN': '********',
            'DJ-Hotspot': '********',
        }
        self.ssid_list = list(self.wifi_list.keys())
        self.screen = screen
        self.current_wifi = ''
        self.select_index = 0
        self.wifi_icon_light_on = False
        self.device = device
        device.add_listener('WIFI_STATUS', self.got_connect_status)

    def got_connect_status(self, data):
        ssid = data['ssid']
        status = data['status']
        if status == 'online':
            self.show_wifi_icon()
            self.current_wifi = ssid
            self.screen.set_page(self._page(), index=0,
                                 reverse_white_row=self.select_index)
        else:
            self.show_wifi_icon()
            self.change_wifi_icon_light()
            self.current_wifi = ''
            self.screen.set_page(self._page(), index=0,
                                 reverse_white_row=self.select_index)

    def _page(self):
        page = []
        for key in self.ssid_list:
            if self.current_wifi == key:
                key = '√' + key
            else:
                key = ' ' + key
            page.append(key)
        return page

    def connect_wifi(self):
        ssid = self.ssid_list[self.select_index]
        password = self.wifi_list[ssid]
        data = {'ssid': ssid, 'password': password}
        self.device.send('CONNECT_WIFI', data)

    def set_wifi_icon(self, signal):
        if signal == '[F6]':  # 切换亮灭
            self.change_wifi_icon_light()
        elif signal == '[F5]':  # 重新请求并根据请求结果刷新
            self.device.send('ASK_WIFI_STATUS', '')

    def show_wifi_icon(self):
        self.screen.show_icon('wifi', 6, 0)
        self.wifi_icon_light_on = True

    def change_wifi_icon_light(self):
        if not self.wifi_icon_light_on:
            self.screen.show_icon('wifi', 6, 0)
            self.wifi_icon_light_on = True
        else:
            self.screen.icon_clean(6, 0)
            self.wifi_icon_light_on = False

    def run(self):
        self.select_index = 0
        self.screen.set_page(self._page(), index=0)
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
            if self.select_index == len(self.ssid_list) - 1:
                return
            self.select_index = self.select_index + 1
        elif event.signal in ['[ENTER]']:
            self.connect_wifi()
        elif event.signal in ['[F5]', '[F6]']:
            self.set_wifi_icon(event.signal)

    def quit(self):
        self.screen.set_reverse_white(False)
