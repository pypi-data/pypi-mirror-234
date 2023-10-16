import json
import time
from typing import Union
from urllib import parse

from filelock import FileLock

from kuto.android import AndroidDriver
from kuto.api import HttpReq
from kuto.ios.driver import IosDriver
from kuto.web.driver import PlayWrightDriver
from kuto.web.element import WebElem
from kuto.mac import MacDriver
from kuto.win import WinDriver

from kuto.utils.config import config, free_config
from kuto.utils.log import logger
from kuto.utils.exceptions import KError


class Page(object):
    """页面基类，用于pom模式封装"""

    def __init__(self, driver):
        self.driver = driver


class Case(HttpReq):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    driver: Union[AndroidDriver, IosDriver,
                  PlayWrightDriver, MacDriver, WinDriver] = None

    # ---------------------初始化-------------------------------
    def start_class(self):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    def end_class(self):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        cls().end_class()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        self.start_time = time.time()
        platform = config.get_common("platform")
        if platform in ["android", "ios"]:
            # 加一段逻辑支持多进程和设备调度
            logger.info("开始获取空闲设备")
            timeout = 30  # 后面再考虑要不要在runner中加一个超时设置
            while timeout > 0:
                with FileLock("session.lock"):
                    device_id = free_config.get_random_device()
                if device_id:
                    logger.info(f"获取空闲设备成功: {device_id}")
                    logger.info(f"剩余空闲设备列表: {free_config.get_all_device()}")
                    break
                logger.info("未找到空闲设备，休息3秒")
                timeout -= 3
                time.sleep(3)
            else:
                logger.info(f"获取空闲设备失败!!!")
                logger.info(f"剩余空闲设备列表: {free_config.get_all_device()}")
                raise KError("获取空闲设备失败!!!")
            if platform == "android":
                pkg_name = config.get_app("pkg_name")
                self.driver = AndroidDriver(device_id=device_id, pkg_name=pkg_name)
            elif platform == "ios":
                pkg_name = config.get_app("pkg_name")
                self.driver = IosDriver(device_id=device_id, pkg_name=pkg_name)
        elif platform == "web":
            browserName = config.get_web("browser_name")
            headless = config.get_web("headless")
            state = config.get_web("state")
            if state:
                state_json = json.loads(state)
                self.driver = PlayWrightDriver(browserName=browserName, headless=headless, state=state_json)
            else:
                self.driver = PlayWrightDriver(browserName=browserName, headless=headless)
        elif platform == "mac":
            pkg_name = config.get_app("pkg_name")
            self.driver = MacDriver(pkg_name=pkg_name)
        elif platform == "win":
            pkg_name = config.get_app("pkg_name")
            self.driver = WinDriver(pkg_name=pkg_name)
        if isinstance(self.driver, (AndroidDriver, IosDriver, MacDriver, WinDriver)):
            if config.get_app("auto_start") is True:
                self.driver.start_app()
        self.start()

    def teardown_method(self):
        self.end()
        if isinstance(self.driver, PlayWrightDriver):
            self.driver.close()
        if isinstance(self.driver, (AndroidDriver, IosDriver, MacDriver, WinDriver)):
            if config.get_app("auto_start") is True:
                self.driver.stop_app()
        if isinstance(self.driver, (AndroidDriver, IosDriver)):
            # 加一段逻辑支持多进程和设备调度
            device_id = self.driver.device_id
            logger.info(f"用例结束释放设备: {device_id}")
            with FileLock("session.lock"):
                devices = free_config.get('devices')
                if device_id not in devices:
                    free_config.add_devices([self.driver.device_id])
            logger.info(f"剩余空闲设备列表: {free_config.get_all_device()}")
        take_time = time.time() - self.start_time
        logger.info("用例耗时: {:.2f} s".format(take_time))

    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.info(f"暂停: {n}s")
        time.sleep(n)

    def open_url(self, url=None):
        """浏览器打开页面"""
        # 拼接域名
        if url is None:
            base_url = config.get_web("base_url")
            if not base_url:
                raise KError('base_url is null')
            url = base_url
        else:
            if "http" not in url:
                base_url = config.get_web("base_url")
                if not base_url:
                    raise KError('base_url is null')
                url = parse.urljoin(base_url, url)
        # 访问页面
        self.driver.open_url(url)
        # 设置cookies
        cookies = config.get_web("cookies")
        if cookies:
            self.driver.set_cookies(cookies)

    def switch_tab(self, **kwargs):
        """切换到新页签，需要先定位导致跳转的元素"""
        locator = WebElem(self.driver, **kwargs)
        self.driver.switch_tab(locator)

    def screenshot(self, name: str):
        """截图"""
        self.driver.screenshot(name)

    # 断言
    def assert_act(self, activity_name: str, timeout=5):
        """断言当前activity，安卓端使用"""
        self.driver.assert_act(activity_name, timeout=timeout)

    def assert_title(self, title: str, timeout=5):
        """断言页面title，web端使用"""
        self.driver.assert_title(title, timeout=timeout)

    def assert_url(self, url: str = None, timeout=5):
        """断言页面url，web端使用"""
        # 拼接域名
        if url is None:
            base_url = config.get_web("base_url")
            if not base_url:
                raise KError('base_url is null')
            url = base_url + "/"
        else:
            if "http" not in url:
                base_url = config.get_web("base_url")
                if not base_url:
                    raise KError('base_url is null')
                url = parse.urljoin(base_url, url)
        self.driver.assert_url(url, timeout=timeout)



