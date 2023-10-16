"""
@Author: kang.yang
@Date: 2023/5/16 14:37
"""
import kuto

from pub import Pub


class TestWebDemo(kuto.Case):

    def start(self):
        self.pub = Pub(self.driver)

    @kuto.title("登录")
    def test_login(self):
        self.open_url()
        self.pub.pwd_login()
        self.assert_url()
        self.screenshot("首页")


if __name__ == '__main__':
    # 直接执行本文件，需要修改conf.yml中的platform
    kuto.main(
        plat="web",
        brow="chrome",
        host="https://www-test.qizhidao.com"
    )

