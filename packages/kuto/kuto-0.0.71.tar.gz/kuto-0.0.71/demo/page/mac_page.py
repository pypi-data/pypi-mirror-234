"""
@Author: kang.yang
@Date: 2023/9/15 10:03
"""
from kuto.mac import Page, ImageElem


class MacPage(Page):
    """根据图片定位，建议使用系统自带截图（shift+command+4）"""

    num_3 = ImageElem(image='../static/calculator_3.png', desc="数字3")
    x = ImageElem(image='../static/calculator_x.png', desc="乘以号")
    num_5 = ImageElem(image='../static/calculator_5.png', desc="数字5")
    equal = ImageElem(image='../static/calculator_=.png', desc="等于")


# class MacPage(kuto.Page):
#     """根据坐标定位，可以使用MacDriver的get_location方法实时获取"""
#     num_3 = CoorElem(coor=(1785, 364), desc="数字3")
#     x = CoorElem(coor=(1833, 369), desc="乘以号")
#     num_5 = CoorElem(coor=(1720, 316), desc="数字3")
#     equal = CoorElem(coor=(1869, 404), desc="等于")
