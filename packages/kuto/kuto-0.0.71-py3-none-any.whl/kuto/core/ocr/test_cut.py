"""
@Author: kang.yang
@Date: 2023/8/19 10:42
"""
import cv2

# 读取图像
image = cv2.imread('./image/20230819103646_ocr识别定位-校园场馆.png')

# 获取图像的宽度和高度
height, width, _ = image.shape

# 计算每个切割区域的宽度和高度
sub_width = width // 2
sub_height = height // 2

# 切割图像成上下左右四个等份
top_left = image[0:sub_height, 0:sub_width]
top_right = image[0:sub_height, sub_width:width]
bottom_left = image[sub_height:height, 0:sub_width]
bottom_right = image[sub_height:height, sub_width:width]

cv2.imwrite('top_left.png', top_left)
