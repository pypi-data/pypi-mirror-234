"""
@Author: kang.yang
@Date: 2023/8/21 17:10
"""
from kuto.android import Page, Elem

"""
图像识别可以配合安卓应用或者IOS应用使用，ios需要加上scale
"""


class ImagePage(Page):
    searchEntry = Elem(rid="com.tencent.mm:id/j5t", desc='搜索框入口')
    searchInput = Elem(rid="com.tencent.mm:id/cd7", desc='搜索框')
    searchResult = Elem(rid="com.tencent.mm:id/kpm", desc="搜索结果")
    schoolEntry = Elem(image="../static/校园场馆.png", desc='校园场馆入口')


