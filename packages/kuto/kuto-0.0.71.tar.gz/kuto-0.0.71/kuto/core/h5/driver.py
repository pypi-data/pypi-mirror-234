import subprocess
import sys
import time
import requests

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException

from kuto.android import AndroidDriver
from kuto.utils.common import screenshot_util
from kuto.utils.log import logger
from kuto.utils.webdriver_manager_extend import ChromeDriverManager


class ChromeConfig:
    headless = False
    options = None
    command_executor = ""


def get_server_chrome_versions():
    """获取淘宝镜像网站上所有的版本列表"""
    version_list = []
    url = "https://registry.npmmirror.com/-/binary/chromedriver/"
    rep = requests.get(url).json()
    for item in rep:
        version_list.append(item["name"])
    return version_list


def get_webview_version(serial_no, pkg_name):
    """通过shell命令获取webview对应chrome的版本号"""
    # 获取应用的pid
    pid = subprocess.getoutput(f"adb -s {serial_no} shell ps | grep {pkg_name}").split(
        " "
    )[6]
    print(pid)

    # 获取webview的socket名称
    socket_name = subprocess.getoutput(
        f"adb -s {serial_no} shell cat /proc/net/unix | grep --binary-file=text webview"
    ).split(" ")[-1][1:]
    print(socket_name)

    # 将webview端口转发到本地
    cmd = f"adb -s {serial_no} forward tcp:5000 localabstract:{socket_name}"
    print(cmd)
    subprocess.getoutput(cmd)

    # 请求本地服务，获取版本号
    version_data = requests.get("http://127.0.0.1:5000/json/version").json()
    print(version_data)
    version = version_data["Browser"].split("/")[1]
    print(version)

    return version


def get_driver_version(serial_no, pkg_name):
    """获取应用对应的淘宝镜像的chromedriver的版本号"""
    webview_version = get_webview_version(serial_no, pkg_name)

    version_list = get_server_chrome_versions()
    if webview_version in version_list:
        return webview_version
    else:
        for version in version_list:
            if version[0:10] == webview_version[0:10]:
                return version.split("/")[0]
        else:
            print("can not found right version in taobao")
            sys.exit()


class H5Driver(object):

    def __init__(self, android_driver: AndroidDriver, timeout=60):
        serial_no = android_driver.device_id
        pkg_name = android_driver.pkg_name

        logger.info(f"start H5Driver for {serial_no}")
        options = webdriver.ChromeOptions()
        options.add_experimental_option("androidDeviceSerial", serial_no)
        options.add_experimental_option("androidPackage", pkg_name)
        options.add_experimental_option("androidUseRunningApp", True)
        options.add_experimental_option("androidProcess", pkg_name)
        for i in range(3):
            logger.debug(f"{i + 1} time try find:")
            try:
                version = get_driver_version(serial_no, pkg_name)
                self.d = webdriver.Chrome(
                    executable_path=ChromeDriverManager(version=version).install(),
                    options=options,
                )
                logger.debug("h5Driver init success.")
                break
            except Exception as e:
                logger.debug(f"{i + 1} times retry")
                time.sleep(3)
        else:
            logger.debug("retry 3 times，h5Driver init fail.")
            sys.exit()

        # 设置页面加载超时时间
        self.d.set_page_load_timeout(timeout)

    @property
    def page_content(self):
        page_source = self.d.page_source
        logger.info(f"get page content: \n{page_source}")
        return page_source

    @property
    def title(self):
        logger.info("get page title")
        title = self.d.title
        logger.info(title)
        return title

    @property
    def url(self):
        logger.info("get page url")
        url = self.d.current_url
        logger.info(url)
        return url

    @property
    def alert_text(self):
        logger.info("get alert text")
        try:
            alert_text = self.d.switch_to.alert.text
        except NoAlertPresentException:
            logger.info(f'no alert')
            return None
        return alert_text

    def open_url(self, url):
        logger.info(f"visit: {url}")
        self.d.get(url)

    def back(self):
        logger.info("back")
        self.d.back()

    def screenshot(self, file_name=None):
        screenshot_util(self.d, file_name=file_name)

    def get_windows(self):
        logger.info(f"get current tab")
        return self.d.window_handles

    def switch_window(self, old_windows):
        logger.info("switch to newest tab")
        current_windows = self.d.window_handles
        newest_window = [
            window for window in current_windows if window not in old_windows
        ][0]
        self.d.switch_to.window(newest_window)

    def switch_to_frame(self, frame_id):
        logger.info(f"switch to frame {frame_id}")
        self.d.switch_to.frame(frame_id)

    def switch_to_frame_out(self):
        logger.info("frame out")
        self.d.switch_to.default_content()

    def execute_js(self, script, *args):
        logger.info(f"exec js script: \n{script}")
        self.d.execute_script(script, *args)

    def click_elem(self, element):
        logger.info(f"click: {element}")
        self.d.execute_script("arguments[0].click();", element)

    def accept_alert(self):
        logger.info("alert accept")
        self.d.switch_to.alert.accept()

    def dismiss_alert(self):
        logger.info("alert dismiss")
        self.d.switch_to.alert.dismiss()
