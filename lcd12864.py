class LCD:
    def __init__(self, CLK, SID):
        self.SID = SID
        self.CLK = CLK
        self.init()

    def init(self):
        # self.draw_clean()
        self._write(0, 0x01)   # 清屏，将DDRAM的地址计数器归零
        self._write(0, 0x0E)   # 显示打开，光标开，光标不反白
        self._write(0, 0x30)   # 8位介面，基本指令集，绘图off
        self._write(0, 0x34)   # 8位介面，进入扩充指令集
        self._write(0, 0x03)   # 扩充指令集，准备重置卷动地址
        self._write(0, 0x40)   # 重置卷动地址
        self._write(0, 0x02)   # 扩充指令集，进制设置卷动地址
        self._write(0, 0x30)   # 回到基本指令集
        self._write(0, 0x02)   # 地址归位
        self._write(0, 0x10)   # 初始化位移

    def _write(self, start, ddata):
        if start == 0:
            start_data = 0xf8  # 写指令
        else:
            start_data = 0xfa  # 写数据

        Hdata = ddata & 0xf0    # 取高四位
        Ldata = (ddata << 4) & 0xf0  # 取低四位

        self._send_byte(start_data)  # 发送起始信号
        self._send_byte(Hdata)  # 发送高四位
        self._send_byte(Ldata)  # 发送低四位

    def _send_byte(self, bbyte):  # 发一个字节
        for i in range(8):
            bit = 0
            if 128 == bbyte & 0x80:
                bit = 1
            self.SID.value(bit)
            self.CLK.value(1)
            self.CLK.value(0)
            bbyte <<= 1

    def _draw_xy(self, x, y, data1, data2):
        self._write(0, 0x80 + y)
        self._write(0, 0x80 + x)
        self._write(1, data1)
        self._write(1, data2)

    def _set_xy(self, x, y):
        address = [0x80+y, 0x90+y, 0x88+y, 0x98+y][x]
        self._write(0, address)

    def display_by_code(self, x, y, code):
        self._set_xy(x, y)
        self._write(1, code)

    def display_char(self, x, y, char):
        self._set_xy(x, y)
        self._write(1, ord(char))

    def display_str(self, x, y, str):
        self._set_xy(x, y)
        for c in str:
            self._write(1, ord(c))

    def display_encode_str(self, x, y, str_gbk_encode):
        self._set_xy(x, y)
        for c in str_gbk_encode:
            self._write(1, c)

    def cursor_off(self):
        self._write(0, 0x0C)

    def cursor_on(self, is_block_cursor = False):
        if is_block_cursor:
            self._write(0, 0x0F)
        else:
            self._write(0, 0x0E)
    
    def cursor_to(self, x, y, is_block_cursor = False):
        self.cursor_off()
        self._write(0, 0x02) # 光标回起点
        self.cursor_on(is_block_cursor)
        if y >=2:
            x += 8
            y -= 2
        for move in range(x + y*16):
            self._write(0, 0x14)

    def draw_clean(self):
        self._write(0, 0x01)   # 清屏
        self._write(0, 0x0C)   # 关闭光标
        self._write(0, 0x36)   # 绘图模式
        for x in range(16):
            for y in range(32):
                self._draw_xy(x, y, 0, 0)
        self._write(0, 0x30)   # 回到基本指令集

    def draw_img_small(self, img):
        # 只显示LCD中间方形区域(64x64)，img有8*64=512个字节
        self._write(0, 0x01)   # 清屏
        self._write(0, 0x0C)   # 关闭光标
        self._write(0, 0x36)   # 绘图模式
        for y in range(32):
            for x in range(4):
                self._draw_xy(x+2, y, img[x * 2 + y * 8],
                              img[x * 2 + y * 8 + 1])
        for y in range(32):
            for x in range(4):
                self._draw_xy(
                    x+10, y, img[256 + x * 2 + y * 8], img[256 + x * 2 + y * 8 + 1])
        self._write(0, 0x30)   # 回到基本指令集

    def draw_img_32(self, x_start, y_start, img = None):
        # 显示32x32图像。img有4*32=128个字节
        # x_start: 0-6, y_start: 0 1 2
        self._write(0, 0x01)   # 清屏
        self._write(0, 0x0C)   # 关闭光标
        self._write(0, 0x36)   # 绘图模式
        if y_start == 0 or y_start == 2:
            x_offset = 4 * y_start
            for y in range(32):
                for x in range(2):
                    fill = (0, 0)
                    if img:
                        fill = (img[x * 2 + y * 4], img[x * 2 + y * 4 + 1])
                    self._draw_xy(x_offset + x + x_start, y, *fill)
        elif y_start == 1:
            for y in range(16):
                for x in range(2):
                    fill_upper_half = (0, 0)
                    fill_lower_half = (0, 0)
                    if img:
                        fill_upper_half = (
                            img[x * 2 + y * 4], img[x * 2 + y * 4 + 1])
                        fill_lower_half = (
                            img[64 + x * 2 + y * 4], img[64 + x * 2 + y * 4 + 1])
                    self._draw_xy(x + x_start, y + 16, *fill_upper_half)
                    self._draw_xy(8 + x + x_start, y, *fill_lower_half)

        self._write(0, 0x30)   # 回到基本指令集

    def draw_row(self, row_no, type='fill'):
        # types: fill/clean
        self._write(0, 0x36)   # 绘图模式
        # self._write(0, 0x03)   # 开卷动
        # self._write(0, 0x40)   # 卷动
        x_offset = [0, 0, 8, 8][row_no]
        y_offset = [0, 16, 0, 16][row_no]
        fill = 0xff
        if type == 'clean':
            fill = 0x00
        for y in range(16):
            for x in range(8):
                self._draw_xy(x + x_offset, y + y_offset, fill, fill)
        # self._write(0, 0x02)   # 关卷动
        self._write(0, 0x30)   # 回到基本指令集

    def draw_row_underline(self, row_no, type='fill', length=8):
        self._write(0, 0x36)   # 绘图模式
        x_offset = [0, 0, 8, 8][row_no]
        y_offset = [15, 31, 15, 31][row_no]
        fill = 0xff
        if type == 'clean':
            fill = 0x00
        for x in range(length):
            self._draw_xy(x + x_offset, y_offset-1, fill, fill)
            self._draw_xy(x + x_offset, y_offset, fill, fill)
        self._write(0, 0x30)   # 回到基本指令集

    def enable_icon_wifi(self, x, y):
        self._write(0, 0x36)   # 绘图模式
        # self._draw_xy(x, y, 0x3e, 0)
        # self._draw_xy(x, y+1, 0x41, 0)
        # self._draw_xy(x, y+2, 0x9c, 0x80)
        # self._draw_xy(x, y+3, 0x22, 0)
        # self._draw_xy(x, y+4, 0x08, 0)
        self._draw_xy(x, y, 0x1f, 0)
        self._draw_xy(x, y+1, 0x20, 0x80)
        self._draw_xy(x, y+2, 0x4e, 0x40)
        self._draw_xy(x, y+3, 0x11, 0)
        self._draw_xy(x, y+4, 0x04, 0)
        self._write(0, 0x30)   # 回到基本指令集

    def enable_icon_battery_incharge(self, x, y):
        self._write(0, 0x36)   # 绘图模式
        self._draw_xy(x, y, 0x00, 0x80)
        self._draw_xy(x, y+1, 0xF9, 0x38)
        self._draw_xy(x, y+2, 0x82, 0x0C)
        self._draw_xy(x, y+3, 0x87, 0x84)
        self._draw_xy(x, y+4, 0x81, 0x0C)
        self._draw_xy(x, y+5, 0xF2, 0x78)
        self._draw_xy(x, y+6, 0x04, 0x00)
        self._write(0, 0x30)   # 回到基本指令集

    def enable_icon_battery(self, x, y):
        self._write(0, 0x36)   # 绘图模式
        self._draw_xy(x, y, 0x00, 0x00)
        self._draw_xy(x, y+1, 0xFF, 0xF8)
        self._draw_xy(x, y+2, 0xFF, 0x8C)
        self._draw_xy(x, y+3, 0xFF, 0x84)
        self._draw_xy(x, y+4, 0xFF, 0x8C)
        self._draw_xy(x, y+5, 0xFF, 0xF8)
        self._draw_xy(x, y+6, 0x00, 0x00)
        self._write(0, 0x30)   # 回到基本指令集
    
    def clean_icon(self, x, y):        
        self._write(0, 0x36)   # 绘图模式
        for i in range(7):
            self._draw_xy(x, y+i, 0x00, 0x00)
        self._write(0, 0x30)   # 回到基本指令集

