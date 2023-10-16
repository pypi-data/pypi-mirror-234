import kuto

from kuto.ios import Case
from page.ios_page import IndexPage, MyPage, SettingPage


class TestIosDemo(Case):
    """IOS应用demo"""

    def start(self):
        self.index_page = IndexPage(self.driver)
        self.my_page = MyPage(self.driver)
        self.set_page = SettingPage(self.driver)

    def test_go_setting(self):
        self.index_page.adBtn.click_exists(timeout=5)
        self.index_page.myTab.click()
        self.my_page.settingBtn.click()
        self.set_page.about.assert_exists()


if __name__ == '__main__':
    """仅执行本模块"""
    from kuto.ios.common import get_connected

    kuto.main(
        devices=get_connected(),
        pkg_name='com.qizhidao.company'
    )


