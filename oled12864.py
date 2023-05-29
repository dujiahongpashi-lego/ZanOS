from machine import Pin
from djhps_i2c_hubno6_mpy_firmware import DJHPS_SoftI2C
from ssd1306_with_framebuf import SSD1306_I2C


def mk_line(x, y, length, x0, y0):
    return (x+x0, y+y0, length + 1, 1)


class OLED:
    def __init__(self, SDAPIN, SCLPIN) -> None:
        self.oled = SSD1306_I2C(128, 64, DJHPS_SoftI2C(SDAPIN, SCLPIN))

    def draw_img_32(self, x_start, y_start, img=None):
        # 显示32x32图像。img有4*32=128个字节
        # x_start: 0-6, y_start: 0 1 2
        if not img:
            return
        self.oled.fill(0)  # clean all
        hlines = []
        for y in range(32):
            line_data = img[4*y:4*y+4]
            # By ChatGPT：
            start, length = None, 0
            lines = []
            for i in range(len(line_data)):
                byte = line_data[i]
                for j in range(7, -1, -1):
                    bit = (byte >> j) & 0x01
                    if bit == 1 and start is None:
                        start = i * 8 + (7 - j)
                        length = 1
                    elif bit == 1:
                        length += 1
                    elif bit == 0 and start is not None:
                        lines.append((start, length))
                        start, length = None, 0

            if start is not None:
                lines.append((start, length))

            for e in lines:
                (x, size) = e
                hlines.append(mk_line(x * 2, y * 2, size * 2, 32, 0))  # 2倍居中显示

        for l in hlines:
            self.oled.hline(*l)

        self.oled.show()
