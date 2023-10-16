"""
@Author: kang.yang
@Date: 2023/8/21 16:38
建议AirtestIDE截图，手机直接截图好像有问题
"""
import kuto

from kuto.android import Case
from page.image_page import ImagePage


class TestImageDemo(Case):
    """图像识别demo"""

    def start(self):
        self.image_page = ImagePage(self.driver)

    def test_nanshan_wtt(self):
        self.image_page.searchEntry.click()
        self.image_page.searchInput.input("南山文体通")
        self.image_page.searchResult.click()
        self.image_page.schoolEntry.click()
        self.sleep(5)


if __name__ == '__main__':
    """仅执行本模块"""
    kuto.main(
        devices=['UJK0220521066836'],
        pkg_name='com.tencent.mm'
    )



