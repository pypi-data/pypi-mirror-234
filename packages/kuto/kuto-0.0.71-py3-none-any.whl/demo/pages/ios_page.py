"""
@Author: kang.yang
@Date: 202
3/8/1 16:27
"""
import kuto


class IndexPage(kuto.Page):
    """首页"""
    adBtn = kuto.Elem(text='close white big')
    myTab = kuto.Elem(text='我的')


class MyPage(kuto.Page):
    """我的页"""
    settingBtn = kuto.Elem(text='settings navi')
