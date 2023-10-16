import time
from typing import Union

from kuto.utils.common import draw_red_by_rect
from kuto.utils.log import logger
from kuto.utils.exceptions import KError

from kuto.android import AndroidDriver
from kuto.ios.driver import IosDriver
from kuto.ios.element import IosElem
from kuto.image.element import ImageElem
from kuto.ocr.element import OCRElem
from kuto.web.element import WebElem, FraElem
from kuto.mac import MacDriver
from requests_toolbelt import MultipartEncoder


class CoorElem(object):
    """根据坐标进行定位"""

    def __init__(self,
                 driver: Union[AndroidDriver, IosDriver, MacDriver] = None,
                 coor: tuple = None,
                 desc: str = None,
                 debug: bool = False):
        self.driver = driver
        if not desc:
            raise KError("元素描述不能为空")
        else:
            self._desc = desc
        self._coor = coor
        self._debug = debug

    def __get__(self, instance, owner):
        if instance is None:
            return None

        self.driver = instance.driver
        return self

    def find(self, timeout=3):
        time.sleep(timeout)
        x, y = self._coor
        if self._debug is True:
            file_path = self.driver.screenshot(f'坐标定位结果-{self._desc}')
            draw_red_by_rect(file_path, (int(x) - 100, int(y) - 100, 200, 200))
        return x, y

    def click(self, timeout=3):
        logger.info(f"点击 {self._desc}")
        x, y = self.find(timeout=timeout)
        self.driver.click(x, y)

    def input(self, text: str, timeout=3):
        logger.info(f"点击 {self._desc}， 输入 {text}")
        x, y = self.find(timeout=timeout)
        self.driver.click(x, y)
        self.driver.input(text)


__all__ = [
    "AndroidDriver",
    "AdrElem",
    "IosDriver",
    "IosElem",
    "ImageElem",
    "OCRElem",
    "WebDriver",
    "WebElem",
    "MacDriver",
    "MacElem",
    "CoorElem",
    "FraElem",
    "HttpReq",
    "MultipartEncoder"
]

