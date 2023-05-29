from machine import UART
import json


class UART2:
    def __init__(self) -> None:
        # init with given baudrate
        self.uart2 = UART(2, 9600)
        self.uart2.init(9600, bits=8, parity=None, stop=1,
                        rxbuf=4096, txbuf=4096)  # init with given parameters
        self.buf = ''

    def read_all(self):
        msg = b''
        r = self.uart2.read()
        while r != None:
            msg += r
            r = self.uart2.read()
        return msg

    def reg_listener(self, cb_list=[{'scope': 'PRINT', 'cb': lambda x: print(x)}]) -> None:
        print('start listen msg')
        while True:
            if self.uart2.any():
                try:
                    msg = self.uart2.read().decode()
                    print(msg)
                    self.buf += msg
                    if self.buf.endswith('DJHPS-MSG-SUFFIX'):
                        data = json.loads(self.buf[:-16])
                        self.buf = ''
                        for cb in cb_list:
                            if data['scope'] == cb['scope']:
                                cb['cb'](data['data'])
                except Exception as e:
                    print(e)

    def response(self, scope, data):
        SUFFIX = 'DJHPS-MSG-SUFFIX'
        msg = json.dumps({'scope': scope, 'data': data})
        self.uart2.write(msg + SUFFIX)
