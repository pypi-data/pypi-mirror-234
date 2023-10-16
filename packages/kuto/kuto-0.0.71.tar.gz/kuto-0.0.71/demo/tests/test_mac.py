"""
@Author: kang.yang
@Date: 2023/9/15 10:19
"""
import kuto

from kuto.mac import Case
from page.mac_page import MacPage


class TestMacDemo(Case):
    """Mac应用demo"""

    def start(self):
        self.mac_page = MacPage(self.driver)

    def test_1(self):
        self.mac_page.num_3.click()
        self.mac_page.x.click()
        self.mac_page.num_5.click()
        self.mac_page.equal.click()
        self.driver.screenshot("计算结果")


if __name__ == '__main__':
    """仅执行本模块"""
    kuto.main(pkg_name='Calculator')
