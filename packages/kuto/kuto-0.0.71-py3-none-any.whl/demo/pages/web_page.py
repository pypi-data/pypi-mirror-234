"""
@Author: kang.yang
@Date: 2023/8/2 20:23
"""
from kuto import Page, Elem


class IndexPage(Page):
    """首页"""
    loginBtn = Elem(text='登录/注册')
    patentText = Elem(text='查专利')


class LoginPage(Page):
    """登录页"""
    pwdLoginTab = Elem(text='帐号密码登录')
    userInput = Elem(holder='请输入手机号码')
    pwdInput = Elem(holder='请输入密码')
    licenseBtn = Elem(css="span.el-checkbox__inner", index=1)
    loginBtn = Elem(text='立即登录')
    firstCompanyIcon = Elem(xpath="(//img[@class='right-icon'])[1]")
