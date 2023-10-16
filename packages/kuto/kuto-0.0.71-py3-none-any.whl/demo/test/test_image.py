"""
@Author: kang.yang
@Date: 2023/8/21 16:38
"""
import kuto
from page.image_page import ImagePage


class TestImageDemo(kuto.Case):
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
    kuto.main(
        plat='android',
        did='UJK0220521066836',
        pkg='com.tencent.mm'
    )



