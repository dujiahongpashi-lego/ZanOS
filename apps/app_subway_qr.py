from zanos import Program
from screen import Screen


class App_Subway_Qr(Program):
    def __init__(self, screen: Screen, d):
        super().__init__(screen)
        self.title = 'JN metro QR'
        self.title_cn = b'\xbc\xc3\xc4\xcf\xb5\xd8\xcc\xfa' # 济南地铁
        self.icon = [0, 0, 0, 0, 0, 0, 0, 0, 63, 255, 255, 252, 63, 255, 255, 252, 48, 1, 128, 12, 48, 1, 128, 12, 51, 249, 159, 204, 51, 249, 159, 204, 51, 25, 152, 204, 51, 25, 152, 204, 51, 25, 152, 204, 51, 249, 159, 204, 51, 249, 159,
                     204, 48, 1, 128, 12, 48, 1, 128, 12, 63, 255, 255, 252, 63, 255, 255, 252, 48, 1, 159, 204, 48, 1, 159, 204, 51, 249, 231, 60, 51, 249, 231, 60, 51, 25, 129, 204, 51, 25, 129, 204, 51, 25, 231, 60, 51, 249, 231, 60, 51,
                     249, 153, 12, 48, 1, 153, 12, 48, 1, 255, 252, 63, 255, 255, 252, 63, 255, 255, 252, 0, 0, 0, 0, 0, 0, 0, 0]
        self.current_files = []
        self.select_index = 0

    def run(self):
        qr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 241, 45, 166, 95, 192, 0, 0, 4, 18, 41, 185, 16, 64, 0, 0, 5, 212, 177, 94, 87, 64, 0, 0, 5, 210, 107, 226, 151, 64, 0, 0, 5, 210, 101, 219, 151, 64, 0, 0, 4, 17, 215, 42, 144, 64, 0, 0, 7, 245, 85, 85, 95, 192, 0, 0, 0, 4, 132, 99, 192, 0, 0, 0, 7, 124, 89, 48, 113, 0, 0, 0, 6, 0, 192, 171, 106, 0, 0, 0, 4, 59, 225, 180, 121, 64, 0, 0, 7, 238, 104, 187, 138, 128, 0, 0, 2, 83, 177, 21, 225, 64, 0, 0, 4, 198, 182, 226, 38, 128, 0, 0, 0, 190, 17, 206, 23, 128, 0, 0, 5, 204, 171, 166, 254, 192, 0, 0, 1, 115, 88, 28, 37, 192, 0, 0, 6, 108, 192, 41, 50, 0, 0, 0, 6, 149, 248, 59, 105, 64, 0, 0, 0, 139, 72, 17, 162, 128, 0, 0, 5, 60, 144, 53, 21, 128, 0, 0, 6, 12, 184, 102, 130,
              0, 0, 0, 5, 251, 51, 175, 67, 128, 0, 0, 4, 45, 143, 31, 136, 64, 0, 0, 2, 122, 73, 9, 84, 192, 0, 0, 0, 42, 196, 59, 171, 192, 0, 0, 5, 120, 215, 25, 197, 128, 0, 0, 2, 6, 88, 166, 222, 192, 0, 0, 5, 95, 167, 85, 124, 192, 0, 0, 0, 7, 164, 20, 197, 64, 0, 0, 7, 244, 25, 95, 84, 64, 0, 0, 4, 21, 163, 47, 71, 0, 0, 0, 5, 214, 80, 15, 125, 192, 0, 0, 5, 211, 193, 81, 246, 128, 0, 0, 5, 214, 221, 11, 97, 192, 0, 0, 4, 23, 112, 66, 170, 192, 0, 0, 7, 244, 223, 71, 6, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.screen.show_img(qr)

    def handle(self, event):
        return super().handle(event)

    def quit(self):
        self.screen.show_img([0] * 512)
