import kuto

from page.adr_page import HomePage, \
    MyPage, SettingPage


class TestAdrDemo(kuto.Case):
    """安卓应用demo"""

    def start(self):
        self.home_page = HomePage(self.driver)
        self.my_page = MyPage(self.driver)
        self.set_page = SettingPage(self.driver)

    def test_1(self):
        self.home_page.myTab.click(timeout=10)
        self.my_page.settingBtn.click()
        self.assert_act('.me.MeSettingActivity')
        self.screenshot("设置页")


if __name__ == '__main__':
    kuto.main(
        plat='android',
        did='UJK0220521066836',
        pkg='com.qizhidao.clientapp'
    )


