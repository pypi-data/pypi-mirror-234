"""
@Author: kang.yang
@Date: 2023/8/2 20:23
"""
from kuto.web import Page, Elem

"""
url相同的页面定义为同一个页面
定位方式：优先使用css，大规模开展自动化前需要开发给相关元素加上唯一标识的测试id
css: 根据cssSelector进行定位，https://zhuanlan.zhihu.com/p/571510714
xpath: 根据xpath进行定位，教程：https://zhuanlan.zhihu.com/p/571060826
text: 根据元素的可视文本内容进行定位
holder: 根据输入框placeHolder进行定位
index: 获取第index个定位到的元素
"""


class IndexPage(Page):
    """首页"""
    loginBtn = Elem(text='登录/注册', desc='登录/注册按钮')
    patentText = Elem(text='查专利', desc='查专利文本')


class LoginPage(Page):
    """登录页"""
    pwdLoginTab = Elem(text='帐号密码登录', desc='账号密码登录tab')
    userInput = Elem(holder='请输入手机号码', desc='账号输入框')
    pwdInput = Elem(holder='请输入密码', desc='密码输入框')
    licenseBtn = Elem(css="span.el-checkbox__inner", index=1, desc='协议选择按钮')
    loginBtn = Elem(text='立即登录', desc='立即登录按钮')
    firstCompanyIcon = Elem(xpath="(//img[@class='right-icon'])[1]", desc='第一家公司')



