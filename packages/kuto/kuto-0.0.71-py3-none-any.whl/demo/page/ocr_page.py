"""
@Author: kang.yang
@Date: 2023/8/21 17:05
"""
from kuto.ios import Page, Elem

"""
ocr识别可以配合安卓应用或者IOS应用进行使用，ios需要加上scale
"""


class OcrPage(Page):
    searchBtn = Elem(text="搜索", className="XCUIElementTypeSearchField", desc='搜索框入口')
    searchInput = Elem(className="XCUIElementTypeSearchField", desc='搜索框')
    searchResult = Elem(xpath="//Table/Cell[2]", desc='搜索结果')
    schoolEntry = Elem(ocr="校园场馆", pos=12, desc="校园场馆入口")

