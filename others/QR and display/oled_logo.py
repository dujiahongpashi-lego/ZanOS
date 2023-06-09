from machine import Pin
from djhps_i2c_hubno6_mpy_firmware import DJHPS_SoftI2C
from machine import SoftI2C
from ssd1306 import SSD1306_I2C
import time

def mk_line(x, y , length,x0, y0):
    return (x+x0, y+y0, length +1, 1)

def draw_smile(oled, start_x, start_y):
    hlines = []
    hlines.append(mk_line(2, 0, 24 - 4, start_x, start_y)) # 上框
    hlines.append(mk_line(2, 30, 24 - 4, start_x, start_y)) # 中线
    hlines.append(mk_line(2, 36, 24 - 4, start_x, start_y)) # 下框
    hlines.append(mk_line(5, 4, 16 - 2, start_x, start_y)) # 屏幕上沿
    hlines.append(mk_line(5, 20, 16 - 2, start_x, start_y)) # 屏幕下沿
    hlines.append(mk_line(4, 25, 1, start_x, start_y)) # 电源
    hlines.append(mk_line(16, 25, 3, start_x, start_y)) # 光驱
    hlines.append(mk_line(10, 16, 3, start_x, start_y)) # 嘴
    
    vlines = []
    vlines.append(mk_line(0, 2, 30 - 4, start_x, start_y)) # 左框1
    vlines.append(mk_line(1, 31, 6 - 2, start_x, start_y)) # 左框2
    vlines.append(mk_line(24, 2, 30 - 4, start_x, start_y)) # 右框1
    vlines.append(mk_line(23, 31, 6 - 2, start_x, start_y)) # 右框2
    vlines.append(mk_line(4, 5, 16 - 2, start_x, start_y)) # 屏幕左沿
    vlines.append(mk_line(20, 5, 16 - 2, start_x, start_y)) # 屏幕右沿
    vlines.append(mk_line(8, 8, 1, start_x, start_y)) # 眼睛
    vlines.append(mk_line(16, 8, 1, start_x, start_y)) # 眼睛
    vlines.append(mk_line(12, 8, 4, start_x, start_y)) # 鼻子
    
    oled.pixel(1 + start_x, 1 + start_y, 1) # 左上角
    oled.pixel(23 + start_x, 1 + start_y, 1) # 右上角
    oled.pixel(1 + start_x, 29 + start_y, 1) # 左下角
    oled.pixel(23 + start_x, 29 + start_y, 1) # 右下角
    oled.pixel(11 + start_x, 12 + start_y, 1) # 鼻钩
    oled.pixel(9 + start_x, 15 + start_y, 1) # 嘴角
    oled.pixel(14 + start_x, 15 + start_y, 1) # 嘴角
    for l in hlines:
        oled.hline(*l)
    for l in vlines:
        oled.vline(*l)
    
def smile_to_sad(oled, start_x, start_y):
    oled.pixel(9 + start_x, 15 + start_y, 0) # 嘴角
    oled.pixel(14 + start_x, 15 + start_y, 0) # 嘴角
    oled.pixel(9 + start_x, 17 + start_y, 1) # 嘴角
    oled.pixel(14 + start_x, 17 + start_y, 1) # 嘴角
    
Pin('A13', Pin.OUT).value(1)# 电池供电

# 创建i2c对象
Pin('C5', Pin.OUT).value(1) # PORT F
i2c = DJHPS_SoftI2C(SDAPIN=Pin('E6'), SCLPIN=Pin('C11'))
i2c = SoftI2C(scl=Pin('C11'), sda=Pin('E6'))

# 创建oled屏幕对象
oled = SSD1306_I2C(128, 64, i2c)
# 在指定位置处显示文字
#oled.text('Hello!', 0, 0, 0xffff)
#oled.text('Hello, World!', 0, 8, 0xffff)
oled.fill(0)

while True:
    #oled.fill(0)
    #draw_smile(oled,54,16)
    #oled.text('Are you OK?', 24, 6, 0xffff)
    #oled.show()
    #time.sleep(5)
    
    #oled.fill(0)
    #draw_smile(oled,54,16)
    #oled.show()
    #time.sleep(5)

    #smile_to_sad(oled,54,16)
    #oled.show()
    #time.sleep(5)
    
    #oled.text('Are you OK?', 24, 6, 0xffff)
    #oled.show()
    #time.sleep(5)
    
    draw_smile(oled,54,16)
    smile_to_sad(oled,54,16)
    oled.text('Are you OK?', 24, 6, 0xffff)
    oled.show()
    time.sleep(60)
    
    

