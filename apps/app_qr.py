from zanos import Program
from screen import Screen


class App_Qr(Program):
    def __init__(self, screen: Screen, d):
        super().__init__(screen)
        self.title = ' QR'
        self.title_cn = b'\xb8\xf7\xce\xbb\xb1\xf0\xc9\xa8'  # 各位别扫
        self.icon = [0, 0, 0, 0, 0, 0, 0, 0, 63, 255, 255, 252, 63, 255, 255, 252, 48, 1, 128, 12, 48, 1, 128, 12, 51, 249, 159, 204, 51, 249, 159, 204, 51, 25, 152, 204, 51, 25, 152, 204, 51, 25, 152, 204, 51, 249, 159, 204, 51, 249, 159,
                     204, 48, 1, 128, 12, 48, 1, 128, 12, 63, 255, 255, 252, 63, 255, 255, 252, 48, 1, 159, 204, 48, 1, 159, 204, 51, 249, 231, 60, 51, 249, 231, 60, 51, 25, 129, 204, 51, 25, 129, 204, 51, 25, 231, 60, 51, 249, 231, 60, 51,
                     249, 153, 12, 48, 1, 153, 12, 48, 1, 255, 252, 63, 255, 255, 252, 63, 255, 255, 252, 0, 0, 0, 0, 0, 0, 0, 0]
        self.select_index = 0
        qr_sub = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 241, 45, 166, 95, 192, 0, 0, 4, 18, 41, 185, 16, 64, 0, 0, 5, 212, 177, 94, 87, 64, 0, 0, 5, 210, 107, 226, 151, 64, 0, 0, 5, 210, 101, 219, 151, 64, 0, 0, 4, 17, 215, 42, 144, 64, 0, 0, 7, 245, 85, 85, 95, 192, 0, 0, 0, 4, 132, 99, 192, 0, 0, 0, 7, 124, 89, 48, 113, 0, 0, 0, 6, 0, 192, 171, 106, 0, 0, 0, 4, 59, 225, 180, 121, 64, 0, 0, 7, 238, 104, 187, 138, 128, 0, 0, 2, 83, 177, 21, 225, 64, 0, 0, 4, 198, 182, 226, 38, 128, 0, 0, 0, 190, 17, 206, 23, 128, 0, 0, 5, 204, 171, 166, 254, 192, 0, 0, 1, 115, 88, 28, 37, 192, 0, 0, 6, 108, 192, 41, 50, 0, 0, 0, 6, 149, 248, 59,
                  105, 64, 0, 0, 0, 139, 72, 17, 162, 128, 0, 0, 5, 60, 144, 53, 21, 128, 0, 0, 6, 12, 184, 102, 130, 0, 0, 0, 5, 251, 51, 175, 67, 128, 0, 0, 4, 45, 143, 31, 136, 64, 0, 0, 2, 122, 73, 9, 84, 192, 0, 0, 0, 42, 196, 59, 171, 192, 0, 0, 5, 120, 215, 25, 197, 128, 0, 0, 2, 6, 88, 166, 222, 192, 0, 0, 5, 95, 167, 85, 124, 192, 0, 0, 0, 7, 164, 20, 197, 64, 0, 0, 7, 244, 25, 95, 84, 64, 0, 0, 4, 21, 163, 47, 71, 0, 0, 0, 5, 214, 80, 15, 125, 192, 0, 0, 5, 211, 193, 81, 246, 128, 0, 0, 5, 214, 221, 11, 97, 192, 0, 0, 4, 23, 112, 66, 170, 192, 0, 0, 7, 244, 223, 71, 6, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        qr_bili_self = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 86, 185, 252, 0, 0, 0, 0, 65, 62, 81, 4, 0, 0, 0, 0, 93, 112, 73, 116, 0, 0, 0, 0, 93, 117, 105, 116, 0, 0, 0, 0, 93, 77, 169, 116, 0, 0, 0, 0, 65, 26, 105, 4, 0, 0, 0, 0, 127, 85, 85, 252, 0, 0, 0, 0, 0, 20, 112, 0, 0, 0, 0, 0, 121, 94, 50, 116, 0, 0, 0, 0, 4, 215, 63, 196, 0, 0, 0, 0, 39, 190, 82, 88, 0, 0, 0, 0, 20, 112, 91, 4, 0, 0, 0, 0, 91, 53, 106, 48, 0, 0, 0, 0, 76, 13, 137, 28, 0, 0, 0, 0, 95, 42, 26, 156,
                        0, 0, 0, 0, 78, 137, 139, 72, 0, 0, 0, 0, 13, 85, 198, 232, 0, 0, 0, 0, 20, 1, 228, 184, 0, 0, 0, 0, 93, 243, 166, 80, 0, 0, 0, 0, 4, 203, 117, 144, 0, 0, 0, 0, 43, 147, 39, 240, 0, 0, 0, 0, 0, 96, 4, 124, 0, 0, 0, 0, 127, 33, 13, 104, 0, 0, 0, 0, 65, 63, 132, 100, 0, 0, 0, 0, 93, 8, 247, 208, 0, 0, 0, 0, 93, 122, 182, 100, 0, 0, 0, 0, 93, 101, 84, 148, 0, 0, 0, 0, 65, 70, 23, 168, 0, 0, 0, 0, 127, 72, 78, 168, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        qr_wx_pay = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 247, 113, 32, 95, 192, 0, 0, 4, 21, 117, 135, 208, 64, 0, 0, 5, 210, 175, 102, 151, 64, 0, 0, 5, 214, 24, 73, 215, 64, 0, 0, 5, 214, 175, 86, 215, 64, 0, 0, 4, 20, 156, 192, 16, 64, 0, 0, 7, 245, 85, 85, 95, 192, 0, 0, 0, 1, 31, 101, 64, 0, 0, 0, 0, 144, 137, 149, 78, 192, 0, 0, 0, 171, 234, 123, 124, 0, 0, 0, 3, 86, 55, 176, 54, 128, 0, 0, 4, 13, 234, 155, 245, 0, 0, 0, 7, 62, 129, 46, 26, 192, 0, 0, 1, 239, 11, 244, 171, 128, 0, 0, 1, 212, 96, 7, 92, 192, 0, 0, 1, 37, 128, 3, 227, 64, 0, 0, 4, 24, 128, 7, 105, 64, 0, 0, 2, 201, 96, 3, 140, 0, 0, 0, 1, 118, 32, 2, 120, 192, 0, 0, 3, 111, 0, 5, 57, 192, 0, 0, 3, 149, 64, 2, 2, 128, 0, 0, 1, 40, 224, 10, 108, 0, 0, 0, 7, 214, 96, 4, 179, 64, 0, 0, 1, 160, 125, 15, 36, 0, 0, 0, 6, 179, 180, 252, 21, 192, 0, 0, 0, 224, 252, 249, 203, 192, 0, 0, 5, 86, 205, 126, 242, 192, 0, 0, 3, 131, 151, 59, 80, 64, 0, 0, 7, 182, 36, 161, 124, 64, 0, 0, 0, 6, 59, 35, 196, 64, 0, 0, 7, 241, 174, 16, 86, 192, 0, 0, 4, 16, 224, 195, 197, 192, 0, 0, 5, 211, 235, 140, 126, 64, 0, 0, 5, 212, 227, 118, 120, 0, 0, 0, 5, 210, 188, 196, 140, 64, 0, 0, 4, 19, 50, 215, 160, 192, 0, 0, 7, 241, 255, 179, 15, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.img_list = [qr_wx_pay, qr_bili_self, qr_sub]

    def run(self):
        self.screen.show_img(self.img_list[self.select_index])

    def handle(self, event):
        if event.signal in ['[ENTER]', '[RIGHT]']:
            self.select_index += 1
            if self.select_index == len(self.img_list):
                self.select_index = 0
        self.screen.show_img(self.img_list[self.select_index])

    def quit(self):
        self.screen.show_img([0] * 512)
