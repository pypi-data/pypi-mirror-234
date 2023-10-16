import time

from typing import Union
from filelock import FileLock

from kuto.api.request import HttpReq
from kuto.ios.driver import Driver
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
        # 加一段逻辑支持多进程和设备调度
        logger.info("开始获取空闲设备")
        timeout = 30  # 后面再考虑要不要在runner中加一个超时设置
        while timeout > 0:
            with FileLock("session.lock"):
                device_id = config.get_random_device()
            if device_id:
                logger.info(f"获取空闲设备成功: {device_id}")
                logger.info(f"剩余空闲设备列表: {config.get_all_device()}")
                break
            logger.info("未找到空闲设备，休息3秒")
            timeout -= 3
            time.sleep(3)
        else:
            logger.info(f"获取空闲设备失败!!!")
            logger.info(f"剩余空闲设备列表: {config.get_all_device()}")
            raise KError("获取空闲设备失败!!!")

        pkg_name = config.get_app("pkg_name")
        self.driver = Driver(device_id=device_id, pkg_name=pkg_name)

        if config.get_app("auto_start") is True:
            self.driver.start_app()
        self.start()

    def teardown_method(self):
        self.end()
        if config.get_app("auto_start") is True:
            self.driver.stop_app()

        # 加一段逻辑支持多进程和设备调度
        device_id = self.driver.device_id
        logger.info(f"用例结束释放设备: {device_id}")
        with FileLock("session.lock"):
            devices = config.get_app('devices')
            if device_id not in devices:
                config.add_devices([self.driver.device_id])
        logger.info(f"剩余空闲设备列表: {config.get_all_device()}")

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




