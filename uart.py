from machine import Pin, UART
import json


class UART_PORT:
    def __init__(self, port='F') -> None:
        p = {
            'A': {'id': 7, 'enable': 'A10'},
            'B': {'id': 4, 'enable': 'A8'},
            'C': {'id': 8, 'enable': 'E5'},
            'D': {'id': 5, 'enable': 'B2'},
            'E': {'id': 10, 'enable': 'B5'},
            'F': {'id': 9, 'enable': 'C5'},
        }[port]
        Pin(p['enable'], Pin.OUT).value(0)  # 使能PORT
        self.uart = UART(p['id'], 9600)
        self.uart.init(9600, bits=8, parity=None, stop=1)
        self.cb_list = []
        self.buf = ''

    def start(self):
        while True:
            if self.uart.any():
                # try:
                msg = self.uart.read().decode()
                print(msg)
                self.buf += msg
                if self.buf.endswith('DJHPS-MSG-SUFFIX'):
                    data = json.loads(self.buf[:-16])
                    self.buf = ''
                else:
                    continue
                for cb in self.cb_list:
                    if data['scope'] == cb['scope']:
                        print('GET:', data['scope'],
                              'callback:', cb, 'data:', data)
                        cb['cb'](data['data'])
                # except Exception as e:
                #    print(e)

    # 注册监听，os和app都可注册。当收到device的消息时，将对应的scope消息调用cb处理
    def add_listener(self, scope, cb):
        self.cb_list.append({'scope': scope, 'cb': cb})

    def _too_long(self, msg):
        MAX = 120
        length = len(msg)
        if length > MAX:
            print(msg)
            print(length, 'TOO LONG!! msg must less then', MAX)

    # 向设备发消息。msg是dict，json转换在这一层完成。
    def send(self, scope, data):
        msg = json.dumps({'scope': scope, 'data': data})
        # if not self._too_long(msg):
        #    self.uart.write(msg)
        SUFFIX = 'DJHPS-MSG-SUFFIX'
        self.uart.write(msg + SUFFIX)
