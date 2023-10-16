"""
@Author: kang.yang
@Date: 2023/8/24 15:56
"""
from page.web_page import IndexPage, LoginPage


class Pub(object):
    """公共方法"""

    def __init__(self, driver):
        self.driver = driver
        self.index_page = IndexPage(self.driver)
        self.login_page = LoginPage(self.driver)

    def pwd_login(self, username="13652435335", password="wz123456@QZD"):
        """账号密码登录流程"""
        self.index_page.loginBtn.click()
        self.login_page.pwdLoginTab.click()
        self.login_page.userInput.input(username)
        self.login_page.pwdInput.input(password)
        self.login_page.licenseBtn.click()
        self.login_page.loginBtn.click()
        self.login_page.firstCompanyIcon.click()
