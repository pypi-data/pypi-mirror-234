import kuto

from kuto.android import Case
from page.adr_page import HomePage, \
    MyPage, SettingPage


class TestAdrDemo(Case):
    """安卓应用demo"""

    def start(self):
        self.home_page = HomePage(self.driver)
        self.my_page = MyPage(self.driver)
        self.set_page = SettingPage(self.driver)

    def test_1(self):
        self.home_page.adBtn.click_exists(timeout=5)
        self.home_page.myTab.click()
        self.my_page.settingBtn.click()
        self.assert_act('.me.MeSettingActivity')
        self.screenshot("设置页")

    # def test_2(self):
    #     self.home_page.adBtn.click_exists(timeout=10)
    #     self.home_page.spaceTab.click()
    #     self.screenshot("科创空间首页")


if __name__ == '__main__':
    """仅执行本模块"""
    kuto.main(
        devices=["UJK0220521066836"],
        pkg_name='com.qizhidao.clientapp',
    )


