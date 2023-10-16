import os.path
import sys


case_content_android = """import kuto
from kuto import AdrElem


class HomePage(kuto.Page):
    ad = AdrElem(resourceId='com.qizhidao.clientapp:id/bottom_btn')
    my = AdrElem(text='我的')


class MyPage(kuto.Page):
    setting = AdrElem(resourceId='com.qizhidao.clientapp:id/me_top_bar_setting_iv')


class TestSetting(kuto.TestCase):

    def start(self):
        self.home_page = HomePage(self.driver)
        self.my_page = MyPage(self.driver)

    def test_1(self):
        self.home_page.ad.click_exists(timeout=5)
        self.home_page.my.click()
        self.my_page.setting.click()


if __name__ == '__main__':
    kuto.main(did='UJK0220521066836', pkg='com.qizhidao.clientapp')

"""

case_content_ios = """import kuto
from kuto import IosElem


class IndexPage(kuto.Page):
    ad = IosElem(text='close white big')
    my = IosElem(text='我的')


class MyPage(kuto.Page):
    setting = IosElem(text='settings navi')


class TestSearch(kuto.TestCase):

    def start(self):
        self.index_page = IndexPage(self.driver)
        self.my_page = MyPage(self.driver)

    def test_1(self):
        self.index_page.ad.click_exists(timeout=5)
        self.index_page.my.click()
        self.my_page.setting.click()


if __name__ == '__main__':
    kuto.main(did='00008101-000E646A3C29003A', pkg='com.qizhidao.company')

"""

case_content_web = """import kuto
from kuto import WebElem


class IndexPage(kuto.Page):
    login = WebElem(text='登录/注册')
    enterprise = WebElem(text='查专利')


class LoginPage(kuto.Page):
    pwdLogin = WebElem(text='帐号密码登录')
    userInput = WebElem(placeholder='请输入手机号码')
    pwdInput = WebElem(placeholder='请输入密码')
    licenseBtn = WebElem(css="span.el-checkbox__inner", index=1)
    loginBtn = WebElem(text='立即登录')


class TestLogin(kuto.TestCase):

    def start(self):
        self.index_page = IndexPage(self.driver)
        self.login_page = LoginPage(self.driver)

    def test_1(self):
        self.open()
        self.index_page.login.click()
        self.login_page.pwdLogin.click()
        self.login_page.userInput.input('xxx')
        self.login_page.pwdInput.input('xxx')
        self.login_page.licenseBtn.click()
        self.login_page.loginBtn.click()
        self.screenshot("登录成功")


if __name__ == '__main__':
    # with open("state.json", "r") as f:
    #     state = json.loads(f.read())

    kuto.main(browser="chrome", host="https://www.qizhidao.com")

"""

case_content_api = """import kuto


class TestHome(kuto.TestCase):

    def test_1(self):
        payload = {"type": 2}
        headers = {"user-agent-web": "X/b67aaff2200d4fc2a2e5a079abe78cc6"}
        self.post('/qzd-bff-app/qzd/v1/home/getToolCardListForPc', json=payload, headers=headers)
        self.assertEq('code', 0)


if __name__ == '__main__':
    kuto.main(
        host='https://app.qizhidao.com'
    )

"""


def create_scaffold(platform):
    """create scaffold with specified project name."""

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    # 新增测试数据目录
    root_path = f"{platform}_demo"
    create_folder(root_path)
    create_folder(os.path.join(root_path, "tests"))
    create_folder(os.path.join(root_path, "report"))
    create_folder(os.path.join(root_path, "data"))
    if platform in ["android", "ios", "web"]:
        create_folder(os.path.join(root_path, "screenshot"))
    # 新增安卓测试用例
    if platform == "android":
        # 新增安卓测试用例
        create_file(
            os.path.join(root_path, "tests", "test_adr.py"),
            case_content_android,
        )

    elif platform == "ios":
        # 新增ios测试用例
        create_file(
            os.path.join(root_path, "tests", "test_ios.py"),
            case_content_ios,
        )
    elif platform == "web":
        # 新增web测试用例
        create_file(
            os.path.join(root_path, "tests", "test_web.py"),
            case_content_web,
        )
    elif platform == "api":
        # 新增接口测试用例
        create_file(
            os.path.join(root_path, "tests", "test_api.py"),
            case_content_api,
        )
    else:
        print("请输入正确的平台: android、ios、web、api")
        sys.exit()
