import cv2 #  pip install opencv-python
import numpy as np

# 读入二维码图像(仅支持点阵小于64x64)(实际像素/点阵尺寸 尽量保证整除)
image = cv2.imread("qr_subway_518x518-37x37.bmp", cv2.IMREAD_GRAYSCALE)
SIZE = 37
prefix_len = 13 # 定义补0的前缀和后缀长度
suffix_len = 14 # 定义补0的前缀和后缀长度

# 读入二维码图像(仅支持点阵小于64x64)(实际像素/点阵尺寸 尽量保证整除)
image = cv2.imread("qr_bili_djhps_261x261-29x29.bmp", cv2.IMREAD_GRAYSCALE)
SIZE = 29
prefix_len = 17 # 定义补0的前缀和后缀长度
suffix_len = 18 # 定义补0的前缀和后缀长度

# 读入二维码图像(仅支持点阵小于64x64)(实际像素/点阵尺寸 尽量保证整除)
image = cv2.imread("qr_wx_pay_555x555-37x37.bmp", cv2.IMREAD_GRAYSCALE)
SIZE = 37
prefix_len = 13 # 定义补0的前缀和后缀长度
suffix_len = 14 # 定义补0的前缀和后缀长度

# 二值化处理，将黑色部分设为0，白色部分设为1
binary_image = np.where(image==0, 0, 1)

# 分割二维码图像，得到黑白方块
num_rows, num_cols = binary_image.shape
block_size = num_rows // SIZE
blocks = []
for r in range(0, num_rows, block_size):
    for c in range(0, num_cols, block_size):
        blocks.append(binary_image[r:r+block_size, c:c+block_size])

# 统计每个方块的像素平均值，判断其为白色还是黑色，并将结果加到二进制字符串中
binary_string = ""
for block in blocks:
    avg_pixel_value = np.mean(block)
    binary_string += "1" if avg_pixel_value < 0.5 else "0"

for i in range(len(binary_string)):  # 循环输出，每SIZE个就换行
    print(binary_string[i], end="") 
    if (i+1) % SIZE == 0: 
        print()
print(len(binary_string))
print(binary_string)




# 在原始字符串中每SIZE个字符断开，并将断开的段放入列表中
str_list = [binary_string[i:i+SIZE] for i in range(0, len(binary_string), SIZE)]

# 对于每个断开的段，补0后再拼接起来
new_str = ""
for segment in str_list:
    # 补前缀0
    prefix = "0" * prefix_len
    # 补后缀0
    suffix = "0" * suffix_len
    # 拼接字符串
    new_str += prefix + segment + suffix

# 输出新的字符串
new_str = "0" *64* prefix_len + new_str + "0" * 64 * suffix_len 
print(new_str)

int_list= []
for i in range(0, len(new_str), 8):
    sub_str = new_str[i:i+8]
    int_list.append(int(sub_str, 2))

print(len(int_list))
print(int_list)