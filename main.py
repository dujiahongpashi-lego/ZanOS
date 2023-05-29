from machine import Pin
from lcd12864 import LCD
from oled12864 import OLED
from ps2 import Keyborad
from screen import Screen
from zanos import ZanOS
from reg import parse_reg
from uart import UART_PORT

# LCD Pin (Port F)
# Pin('C5', Pin.OUT).value(1)  # init PORT F
# SID = Pin('C11', Pin.OUT)  # R/W
# CLK = Pin('E6', Pin.OUT)  # E

# LCD Pin (Port B)
Pin('A8', Pin.OUT).value(1)  # init PORT B
SID = Pin('D9', Pin.OUT)  # R/W
CLK = Pin('D10', Pin.OUT)  # E

# OLED Pin (Port C)
Pin('E5', Pin.OUT).value(1)  # init PORT C
SDA = Pin('E4', Pin.OUT)
SCL = Pin('D11', Pin.OUT)

# KEYBOARD Pin (Port D)
Pin('B2', Pin.OUT).value(1)  # init PORT D
KEY_CLK = Pin('C15', Pin.IN)
KEY_DATA = Pin('C14', Pin.IN)

# UART (Port F)
esp32_device = UART_PORT('F')

screen = Screen(LCD(CLK, SID), OLED(SDA, SCL))
cn = False
cn = True
os = ZanOS(screen, esp32_device, cn)
os.set_menu(parse_reg())
Keyborad(KEY_CLK, KEY_DATA, cb=os.signal_trigger)

os.boot()
