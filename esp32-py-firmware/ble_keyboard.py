import bluetooth  # 导入BLE功能模块
from micropython import const
import time
import binascii

KEYBOARD_ADDR = '68:78:56:'

_IRQ_CONNECTION_UPDATE = const(27)
_IRQ_SCAN_RESULT = 5
_IRQ_SCAN_DONE = 6
_IRQ_PERIPHERAL_CONNECT = 7
_IRQ_PERIPHERAL_DISCONNECT = 8
_IRQ_GATTC_NOTIFY = 18

Key_Map = {
    40: '[ENTER]',
    41: '[ESC]',
    42: '[BACKSPACE]',
    44: ' ',
    45: '-',
    46: '=',
    54: ',',
    55: '.',
    56: '/',
    57: '[CAPSLOCK]',
    79: '[RIGHT]',
    80: '[LEFT]',
    81: '[DOWN]',
    82: '[UP]',
}


class BLEKeyboard:
    def __init__(self, on_success, on_fail, on_key_press):
        ble = bluetooth.BLE()
        ble.active(True)

        self._ble = ble
        self._ble.irq(self._irq)
        self._conn_handle = None
        self._rx_handle = None

        self.on_success = on_success
        self.on_fail = on_fail
        self.on_key_press = on_key_press

    # Connect to the specified device (otherwise use cached address from a scan).

    def connect(self, addr_type=None, addr=None, callback=None):
        self._addr_type = addr_type or self._addr_type
        self._addr = addr or self._addr
        self._conn_callback = callback
        if self._addr_type is None or self._addr is None:
            return False
        print('Try to connect...', self._addr_type, self._addr)
        self._ble.gap_connect(self._addr_type, self._addr)
        return True

    # Returns true if we've successfully connected and discovered uart characteristics.
    def is_connected(self):
        return (
            self._conn_handle is not None
            and self._rx_handle is not None
        )

    # Disconnect from current device.
    def disconnect(self):
        print('Try disconnect ', self._conn_handle)
        if self._conn_handle is None:
            print('error, not found conn_handle')
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._conn_handle = None

    def _on_scan(self, addr_type, addr_show_addr, addr):
        if addr_type is not None:
            print("Found peripheral:", addr_show_addr)
            self.connect()
        else:
            self.timed_out = True
            print("No uart peripheral '{}' found.".format(KEYBOARD_ADDR))

    # Find a device advertising the uart service.
    def scan(self, callback=None):
        self._addr_type = None
        self._addr = None
        self._addr_show_str = None
        self._scan_callback = callback
        self._ble.active(False)
        print('Start Scan')
        time.sleep_ms(1000)
        self._ble.active(True)
        self._ble.gap_scan(20000, 30000, 30000)

    def scan_connect(self):
        self.timed_out = False
        self.scan(callback=self._on_scan)
        # while not self.is_connected() and not self.timed_out:
        #     time.sleep_ms(10)
        # return not self.timed_out

    def _irq(self, event, data):
        # print('Event', event)
        if event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            print('Connect successful.', conn_handle)
            if addr_type == self._addr_type and addr == self._addr:
                self._conn_handle = conn_handle
        elif event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            addr_str = binascii.hexlify(addr).decode('utf-8')
            print(addr_str)
            if addr_str.startswith(KEYBOARD_ADDR.lower().replace(':', '')):
                print('Found one!', addr_str, addr_str)
                self._addr_type = addr_type
                self._addr_show_str = addr_str
                self._addr = bytes(addr)
                self._ble.gap_scan(None)
        elif event == _IRQ_SCAN_DONE:
            print('Scan Done')
            time.sleep_ms(100)
            if self._scan_callback:
                if self._addr:
                    self._scan_callback(
                        self._addr_type, self._addr_show_str, self._addr)
                    self._scan_callback = None
                else:
                    self._scan_callback(None, None, None)
        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            print('Connection Miss!')
            self.on_fail()
        elif event == _IRQ_CONNECTION_UPDATE:
            print('Connection Update! Keyboard Ready! Use it!')
            self.on_success()
        elif event == _IRQ_GATTC_NOTIFY:  # 获取到了广播数据
            conn_handle, value_handle, notify_data = data
            data = bytes(notify_data)
            if data == b'd':  # 心跳信号
                return
            key = self.get_hid_key(bytes(notify_data))
            if key:
                print(key)
                self.on_key_press(key)

    def get_hid_key(self, data):
        print(data)
        """
        解析hid协议的键盘按键产生的数据

        HID设备发给HID主机的数据为8个字节
        第一个字节是Modifier按键,相应的位为1表示对应的按键按下(GUI在Windows下是Win键)
        第一字节8个bit:
        左ctrl 左shift 左alt 左GUI 右ctrl 右shift 右alt 右GUI 

        第二个字节保留,默认为零
        第三到第八字节可表示六个按键,数据值为零表示无按键按下,按键对应的代码可搜索HID KeyCode
        比如按键A对应的代码是0x04,按键B对应的代码是0x05,Enter键对应的代码是0x28

        比如：
        0x80,0x00,0x06,0x00,0x00,0x00,0x00,0x00 表示同时按下Ctrl键和字母C键。
        0x40,0x00,0x04,0x00,0x00,0x00,0x00,0x00 表示同时按下Shift键和字母A键。
        需要注意的是,收到按键按下的数据后,会跟随收到按键抬起的数据
        """
        # 解析键码
        code_modifier = data[0]
        code = data[2]

        if code_modifier == 0 and code == 0:  # 过滤抬起或不支持的按键
            return ''
        if code == 0:  # Modifier按键
            if code_modifier == 1 or code_modifier == 8: # 0x01 0x10
                return '[CTRL]'
            if code_modifier == 128: # 0x80
                return '[WIN]'
        if code >= 4 and code <= 29:  # 26个字母
            char = chr(code + 93)
            if code_modifier == 2 or code_modifier == 32:  # 同时按下了shift. 0x02 0x20
                char = chr(code + 61)
            return char
        elif code >= 30 and code <= 38:  # 数字1-9
            return chr(code + 19)
        elif code == 39:  # 数字0
            return '0'
        elif code >= 58 and code <= 69:  # F1-F12
            return '[F' + str(code-57) +']'
        elif code in Key_Map.keys():  # 其他按键
            return Key_Map[code]

        return ''
