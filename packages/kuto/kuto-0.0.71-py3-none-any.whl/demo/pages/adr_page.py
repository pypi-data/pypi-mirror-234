"""
@Author: kang.yang
@Date: 2023/8/1 11:53
"""
from kuto import Page, Elem


class DemoPage(Page):
    """定位方式展示"""
    loc_by_rid = Elem(rid="com.qizhidao.clientapp:id/ivScan")
    loc_by_text = Elem(text="我的")
    loc_by_cname = Elem(cname="android.widget.ImageView", index=1)
    loc_by_xpath = Elem(xpath='//*[@resource-id="com.qizhidao.clientapp'
                              ':id/llBottomTabs"]/android.widget.FrameLayout[4]')


class HomePage(Page):
    """APP首页"""
    adBtn = Elem(rid='com.qizhidao.clientapp:id/bottom_btn')
    myTab = Elem(xpath='//*[@resource-id="com.qizhidao.clientapp:id/ll'
                    'BottomTabs"]/android.widget.FrameLayout[4]')


class MyPage(Page):
    """我的页"""
    settingBtn = Elem(rid='com.qizhidao.clientapp:id/me_top_bar_setting_iv')


class SettingPage(Page):
    """设置页"""
    title = Elem(rid='com.qizhidao.clientapp:id/tv_actionbar_title')
    agreementText = Elem(rid='com.qizhidao.clientapp:id/agreement_tv_2')
