import time
from machine import Pin

# 定义码字典
key_dict = {
    0x1C: 'a', 0x32: 'b', 0x21: 'c', 0x23: 'd', 0x24: 'e', 0x2B: 'f', 0x34: 'g', 0x33: 'h',
    0x43: 'i', 0x3B: 'j', 0x42: 'k', 0x4B: 'l', 0x3A: 'm', 0x31: 'n', 0x44: 'o', 0x4D: 'p',
    0x15: 'q', 0x2D: 'r', 0x1B: 's', 0x2C: 't', 0x3C: 'u', 0x2A: 'v', 0x1D: 'w', 0x22: 'x',
    0x35: 'y', 0x1A: 'z', 0x45: '0', 0x16: '1', 0x1E: '2', 0x26: '3', 0x25: '4', 0x2E: '5',
    0x36: '6', 0x3D: '7', 0x3E: '8', 0x46: '9', 0x29: ' ',
    0x0D: '[TAB]', 0x59: '[SHIFT]',  # 0x12:'[LEFT SHIFT]',
    0x66: '[BACKSPACE]', 0x5A: '[ENTER]', 0x14: '[CTRL]', 0x11: '[ALT]', 0x1F: '[WIN]',
    0x58: '[CAPSLOCK]',  0x2F: '[MOUSERIGHTCLICK]', 0x40: '[COMPUTER]',
    0x76: '[ESC]', 0x0E: '~', 0x0F: '[TAB]', 0x4E: '-', 0x55: '=', 0x5D: '\\',
    0x54: '[',  0x5B: ']', 0x4C: ';', 0x52: '\'', 0x41: ',', 0x49: '.', 0x4A: '?',#'/',
    0x75: '[UP]', 0x72: '[DOWN]', 0x6B: '[LEFT]', 0x74: '[RIGHT]',
    0x05: '[F1]', 0x06: '[F2]', 0x04: '[F3]', 0x0C: '[F4]', 0x03: '[F5]', 0x0B: '[F6]',
    0x83: '[F7]', 0x0A: '[F8]', 0x01: '[F9]', 0x09: '[F10]', 0x78: '[F11]', 0x07: '[F12]',
    0x7C: '[PRTSCN]', 0x7E: '[SCRLK]', 0xE1: '[PAUSEBREAK]',
    0x6C: '[HOME]', 0x69: '[END]',  0x70: '[INSERT]', 0x7D: '[PAGEUP]', 0x71: '[DELETE]', 0x7A: '[PAGEDOWN]',
    0x77: '[NUMLOCK]', 0x7C: '*', 0x7B: '-', 0x79: '+', 0x73: '[FIVE]',
}


class Keyborad:
    def __init__(self, clk_pin, data_pin, cb):
        self.cb = cb
        self.data_pin = data_pin
        self.counter = 0
        self.buffer = []
        self.start_time = 0
        self.filter_start_time = 0
        self.caps_lock = False
        clk_pin.irq(self.read_bit, Pin.IRQ_FALLING)

    def init_buffer(self):
        self.counter = 0
        self.buffer = []

    def filter_key(self, key_signals):
        if key_signals == '[Key_Release]':
            return False

        return True

    def get_key(self):
        byte = 0
        for i in range(1, 9):
            byte |= self.buffer[i] << (i-1)
        if byte in key_dict.keys():
            return key_dict[byte]
        elif byte == 240:
            return '[Key_Release]'
        return hex(byte)

    def read_bit(self, _something_useless):
        current = time.time_ns()
        space_time = current - self.start_time
        self.start_time = current
        # print(space_time)
        if space_time > 10000000:  # 新的一轮开始
            self.init_buffer()
        bit = self.data_pin.value()
        self.counter += 1

        self.buffer.append(bit)
        if self.counter == 11:
            key = self.get_key()
            # 控制命令(这样的问题是会忽略掉左shift键，且无法区分哪些是命令哪些是按键)
            if key == '0xe0' or key == '0x12':
                self.init_buffer()
                return

            if self.filter_key(key):
                if key == '[CAPSLOCK]':
                    self.caps_lock = not self.caps_lock
                if  self.caps_lock and len(key) == 1 and key.isalpha() and key.islower():
                    key = key.upper()
                self.cb('ps2', key)

