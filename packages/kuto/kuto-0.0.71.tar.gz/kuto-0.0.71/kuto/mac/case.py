import time
from typing import Union

from kuto.mac.driver import Driver
from kuto.api.request import HttpReq

from kuto.utils.config import config
from kuto.utils.log import logger


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

        pkg_name = config.get_app("pkg_name")
        self.driver = Driver(pkg_name=pkg_name)

        if config.get_app("auto_start") is True:
            self.driver.start_app()

        self.start()

    def teardown_method(self):
        self.end()

        if config.get_app("auto_start") is True:
            self.driver.stop_app()

        take_time = time.time() - self.start_time
        logger.info("用例耗时: {:.2f} s".format(take_time))

    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.info(f"暂停: {n}s")
        time.sleep(n)

    def screenshot(self, name: str):
        """截图"""
        self.driver.screenshot(name)




