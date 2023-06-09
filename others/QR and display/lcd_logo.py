from machine import Pin
import time

# init Port
PWR = Pin('A14', Pin.OUT)
Pin('C5', Pin.OUT).value(1) # PORT F
Pin('B2', Pin.OUT).value(1) # PORT D

# 4 Pin
#RST = Pin('C11', Pin.OUT, Pin.PULL_DOWN) # RST PORT F p5
#CS = Pin('C15', Pin.OUT , Pin.PULL_DOWN) # RS PORT D p5
#SID = Pin('C14', Pin.OUT, Pin.PULL_DOWN) # R/W PORT D p6
#CLK = Pin('E6', Pin.OUT, Pin.PULL_DOWN) # E PORT F p6

# 2 Pin
SID = Pin('C11', Pin.OUT) # R/W
CLK = Pin('E6', Pin.OUT) # E


def LCD_send_byte(bbyte):  # 发一个字节
    for i in range(8):
        bit = 0
        if 128 == bbyte & 0x80:
            bit = 1
        SID.value(bit)
        time.sleep_us(4)
        CLK.value(1)
        time.sleep_us(4)
        CLK.value(0)  
        time.sleep_us(4)
        bbyte <<= 1


#  //写指令或数据
# start为1表示数据是显示数据，为0表示数据是控制指令。不支持读数据
def LCD_write(start, ddata):
    if start == 0:
        start_data = 0xf8  # 写指令
    else:
        start_data = 0xfa  # 写数据

    Hdata = ddata & 0xf0    # 取高四位
    Ldata = (ddata << 4) & 0xf0  # 取低四位

    #CS.value(1)
    time.sleep_us(15)
    LCD_send_byte(start_data)  # 发送起始信号
    LCD_send_byte(Hdata)  # 发送高四位
    LCD_send_byte(Ldata)  # 发送低四位
    time.sleep_us(15)
    #CS.value(0)


def LCD_init():
    #RST.value(0)
    #RST.value(1)  # 复位LCD
    #CS.value(0)
    #PWR.off()
    #PWR.on()
    LCD_write(0, 0x01)   # 清屏，将DDRAM的地址计数器归零
    LCD_write(0, 0x0E)   # 显示打开，光标开
    LCD_write(0, 0x30)   # 8位介面，基本指令集


def LCD_set_xy(x, y):
    address = [0x80+y, 0x90+y, 0x88+y, 0x98+y][x]
    LCD_write(0, address)


def LCD_display_by_code(x, y, code):
    LCD_set_xy(x, y)
    LCD_write(1, code)


def LCD_display_char(x, y, char):
    LCD_set_xy(x, y)
    LCD_write(1, ord(char))


def LCD_display_str(x, y, str_gbk_encode):
    LCD_set_xy(x, y)
    for c in str_gbk_encode:
        print(c)
        LCD_write(1, c)

import struct
def LCD_display_cn(x, y, str):
    LCD_set_xy(x, y)
    for c in str:
        print(c, ord(c),ord(c).to_bytes(2, 'big'))
        for b in ord(c).to_bytes(3, 'little'):
            LCD_write(1, b)


LCD_init()
LCD_display_char(0, 1, 'e')
LCD_display_by_code(0, 0, 75)
LCD_display_str(1, 0, b'\xc4\xe3\xba\xc3\xca\xc0\xbd\xe7') # GBK/GB2312
LCD_display_cn(2, 0, '是什么') # GBK/GB2312
LCD_display_str(3, 0, b'\xc4\xe3\xba\xc3\xca\xc0\xbd\xe7') # GBK/GB2312



