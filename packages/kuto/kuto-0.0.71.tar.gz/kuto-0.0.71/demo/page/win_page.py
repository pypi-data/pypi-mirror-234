"""
@Author: kang.yang
@Date: 2023/9/20 10:53
"""
from kuto.win import Page, Elem


class WinPage(Page):
    num_3 = Elem(image='../static/calculator_3_win.png', desc="数字3")
    x = Elem(image='../static/calculator_x_win.png', desc="乘以号")
    num_5 = Elem(image='../static/calculator_5_win.png', desc="数字5")
    equal = Elem(image='../static/calculator_=_win.png', desc="等于")
