"""
@Author: kang.yang
@Date: 2023/7/31 18:14
"""
from kuto.android import Driver, Elem

driver = Driver(device_id='UJK0220521066836', pkg_name='com.qizhidao.clientapp')
driver.start_app()
Elem(driver, rid='com.qizhidao.clientapp:id/btn_login').click()
Elem(driver, text='其他手机号码登录').click()
Elem(driver, text='帐号密码登录').click()
Elem(driver, rid='com.qizhidao.clientapp:id/phone_et').input_exists("13652435335")
Elem(driver, rid='com.qizhidao.clientapp:id/clear_edit_text').input_pwd("wz123456@QZD")
Elem(driver, rid='com.qizhidao.clientapp:id/pwd_check_box_layout').click_exists()
Elem(driver, text='登录').click()
Elem(driver, rid='com.qizhidao.clientapp:id/common_list_rv').click_exists()
Elem(driver, rid='com.qizhidao.clientapp:id/skip_btn').click_exists()
driver.assert_act('.main.HomeActivity')
driver.stop_app()
