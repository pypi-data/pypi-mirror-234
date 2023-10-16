"""
@Author: kang.yang
@Date: 2023/5/16 14:37
"""
import kuto

from kuto.web import Case
from pub import Pub


class TestWebDemo(Case):

    def start(self):
        self.pub = Pub(self.driver)

    @kuto.title("登录")
    def test_login(self):
        self.open_url()
        self.pub.pwd_login()
        self.assert_url()
        self.screenshot("首页")


if __name__ == '__main__':
    """仅执行本模块"""
    kuto.main(host="https://www-test.qizhidao.com")


