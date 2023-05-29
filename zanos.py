import time
from icons import zan
from screen import Screen
from uart import UART_PORT
from power import Battery


class EVENT_TYPE:
    COMMAND = 1
    CHAR_INPUT = 2


class EVENT_SCOPE:
    OS = 1
    APP = 2


class Event:
    evt_type = EVENT_TYPE.COMMAND
    evt_scope = EVENT_SCOPE.APP
    signal = ''


class Program:
    def __init__(self, screen: Screen, device: UART_PORT = None):
        self.screen = screen
        self.device = device
        self.title = ''
        self.title_cn = ''
        self.icon = None

    def run(self):
        pass

    def handle(self, event: Event):
        pass

    def quit(self):
        pass


class MenuItem:
    def __init__(self, name, title, icon, program: Program):
        self.name = name
        self.icon = icon
        self.title = title
        self.program = program


class ZanOS:
    def __init__(self, screen: Screen, device: UART_PORT, cn=False):
        self.screen = screen
        self.program = None
        self.currentMenu = 0
        self.currentState = 'menu'
        self.menu = [
            MenuItem('app', 'APP', None, None)
        ]
        self.cn_enable = cn
        self.device = device
        self.battery_icon = ''

    def boot(self):
        # Battery().enable_battery_power()
        self.show_boot_screen()
        self.init_menu()
        self.device.add_listener(
            'KEYBOARD_STATUS', self.ble_keyboard_status_trigger)
        self.device.add_listener('KEY_PRESSED', self.on_ble_key_event)
        self.device.start()
        while True:
            pass

    def show_boot_screen(self):
        if self.cn_enable:
            self.screen.show_img(zan, '32', 2, 1)
            self.screen.set_line(2, b'        \xd4\xdeOS')
        else:
            self.screen.show_img(zan, '32', 1, 1)
            self.screen.set_line(2, '       Zan OS')
        time.sleep(2)
        self.screen.set_page(['', '', '', ''])
        self.screen.show_img(None, 'blank32', 1, 1)

    def set_battery_icon(self, i):
        if i == 'i':
            self.screen.show_icon('battery_i', 7, 0)
        elif i == 'b':
            self.screen.show_icon('battery', 7, 0)
        else:
            self.screen.icon_clean(7, 0)

    def set_menu(self, menuitems):
        self.menu = []
        for item in menuitems:
            # 初始化app，并将screen注册给app
            app = item['app'](self.screen, self.device)
            title = app.title
            if self.cn_enable:
                title = app.title_cn
            self.menu.append(MenuItem(item['name'], title, app.icon, app))

    def init_menu(self):
        self.currentMenu = 0
        self.currentState = 'menu'
        item = self.menu[0]
        self._show_menu_item(item.title, item.icon,
                             left_en=False, right_en=True)
        self.battery_icon = 'b'
        self.set_battery_icon(self.battery_icon)

    def quit_menu(self):
        self.screen.set_page(['', '', '', ''])
        self.screen.show_img(None, 'blank32', 3, 1)

    def _show_menu_item(self, title, img, left_en, right_en):
        self.screen.show_img(img, '32', 3, 1)
        self.screen.set_line(3, title, centered='True')
        if left_en:
            self.screen.set_line(2, ' <              ')
        elif right_en:
            self.screen.set_line(2, '              > ')
        if left_en and right_en:
            self.screen.set_line(2, ' <            > ')

    def change_menu(self, direction):
        # direction 1 or -1
        current = self.currentMenu + direction
        left_en = True
        right_en = True
        if current < 0 or current == 0:
            current = 0
            left_en = False
        elif current >= len(self.menu) - 1:
            current = len(self.menu) - 1
            right_en = False

        menu_item = self.menu[current]
        self.currentMenu = current
        self._show_menu_item(menu_item.title, menu_item.icon,
                             left_en, right_en)

    def run_program(self, id):
        program = self.menu[id].program
        self.program = program
        self.currentState = self.menu[id].name
        self.quit_menu()
        program.run()

    def quit_program(self):
        self.program.quit()
        self.program = None
        self.currentState = 'menu'
        self.init_menu()

    def handle_os_event(self, event):
        if self.currentState == 'menu' and event.signal in ['[HOME]', '[WIN]', '[COMPUTER]', '[ESC]']:
            self.init_menu()
        elif self.currentState == 'menu' and event.signal in ['[F1]']:
            self.device.send('CONNECT_KEYBOARD', '')
            self.screen.debug(b'\xc0\xb6\xd1\xc0\xbc\xfc\xc5\xcc',
                              b'\xc9\xa8\xc3\xe8\xd6\xd0')  # 蓝牙键盘 扫描中
        elif self.currentState == 'menu' and event.signal in ['[F2]']:
            self.screen.debug()  # debug clean
        elif self.currentState == 'menu' and event.signal in ['[F3]']:
            if self.battery_icon == '':
                self.battery_icon = 'b'
            elif self.battery_icon == 'b':
                self.battery_icon = 'i'
            else:
                self.battery_icon = ''
            self.set_battery_icon(self.battery_icon)

    def menu_handle_input(self, event):
        if event.signal in ['[LEFT]', '[UP]']:
            self.change_menu(-1)
        elif event.signal in ['[RIGHT]', '[DOWN]']:
            self.change_menu(1)

    def check_update_state(self, event) -> bool:
        print(self.currentState, event.signal)
        if self.currentState == 'menu' and event.signal in ['[ENTER]']:
            self.run_program(self.currentMenu)
            return True
        if self.currentState != 'menu' and event.signal in ['[HOME]', '[WIN]', '[COMPUTER]', '[ESC]']:
            self.quit_program()
            return True
        return False

    def get_key_event(self, signal) -> Event:
        e = Event()
        e.signal = signal
        e.evt_type = EVENT_TYPE.CHAR_INPUT
        e.evt_scope = EVENT_SCOPE.APP
        if len(signal) != 1:
            e.evt_type = EVENT_TYPE.COMMAND
            if signal in ['[F1]', '[F2]', '[F3]', '[CAPSLOCK]', '[HOME]', '[WIN]', '[COMPUTER]', '[ESC]']:
                e.evt_scope = EVENT_SCOPE.OS

        return e

    def signal_trigger(self, device, signal):
        event = None # event对象有点过度设计
        if device == 'ps2' or device == 'ble':
            event = self.get_key_event(signal)

        # 优先切换状态
        # 其次，未切换状态则接收OS级别命令
        # 再次，非OS级别命令，则传给当前程序处理（若未运行程序则由菜单处理）
        if event and not self.check_update_state(event):
            if event.evt_scope == EVENT_SCOPE.OS:
                self.handle_os_event(event)
            elif self.program and self.currentState != 'menu':
                self.program.handle(event)
            else:
                self.menu_handle_input(event)

    def on_ble_key_event(self, key):
        self.signal_trigger('ble', key)

    def ble_keyboard_status_trigger(self, msg):
        if msg == 'READY':
            self.screen.debug('', b'\xd2\xd1\xbe\xcd\xd0\xf7')  # 已就绪
        elif msg == 'MISS':
            self.screen.debug('', b'\xd0\xe8\xd6\xd8\xc1\xac')  # 需重连
