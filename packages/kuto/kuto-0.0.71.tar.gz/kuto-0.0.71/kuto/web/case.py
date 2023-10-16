import json
import time

from typing import Union
from urllib import parse

from kuto.web.driver import Driver
from kuto.web.element import Elem
from kuto.api.request import HttpReq

from kuto.utils.config import config
from kuto.utils.log import logger
from kuto.utils.exceptions import KError


class Case(HttpReq):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    driver: Union[Driver] = None

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

        browserName = config.get_web("browser_name")
        headless = config.get_web("headless")
        # state = config.get_web("state")
        # if state:
        #     state_json = json.loads(state)
        #     self.driver = Driver(browserName=browserName, headless=headless, state=state_json)
        # else:
        self.driver = Driver(browserName=browserName, headless=headless)

        self.start()

    def teardown_method(self):
        self.end()

        self.driver.close()

        take_time = time.time() - self.start_time
        logger.info("用例耗时: {:.2f} s".format(take_time))

    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.info(f"暂停: {n}s")
        time.sleep(n)

    def open_url(self, url=None, cookies=None):
        """浏览器打开页面"""
        # 拼接域名
        if url is None:
            base_url = config.get_common("base_url")
            if not base_url:
                raise KError('base_url is null')
            url = base_url
        else:
            if "http" not in url:
                base_url = config.get_common("base_url")
                if not base_url:
                    raise KError('base_url is null')
                url = parse.urljoin(base_url, url)
        # 访问页面
        self.driver.open_url(url)

        # 设置cookies
        if cookies:
            self.driver.set_cookies(cookies)

    def switch_tab(self, **kwargs):
        """切换到新页签，需要先定位导致跳转的元素"""
        locator = Elem(self.driver, **kwargs)
        self.driver.switch_tab(locator)

    def screenshot(self, name: str):
        """截图"""
        self.driver.screenshot(name)

    def assert_title(self, title: str, timeout=5):
        """断言页面title，web端使用"""
        self.driver.assert_title(title, timeout=timeout)

    def assert_url(self, url: str = None, timeout=5):
        """断言页面url，web端使用"""
        # 拼接域名
        if url is None:
            base_url = config.get_common("base_url")
            if not base_url:
                raise KError('base_url is null')
            url = base_url + "/"
        else:
            if "http" not in url:
                base_url = config.get_common("base_url")
                if not base_url:
                    raise KError('base_url is null')
                url = parse.urljoin(base_url, url)
        self.driver.assert_url(url, timeout=timeout)



