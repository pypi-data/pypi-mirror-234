"""
@Author: kang.yang
@Date: 2023/9/14 19:34
"""
import time

from kuto.win import WinDriver
from kuto.utils.exceptions import KError
from kuto.utils.log import logger
from kuto.utils.common import draw_red_by_rect


class WinElem(object):
    """windows元素定位"""

    def __init__(self,
                 driver: WinDriver = None,
                 image: str = None,
                 desc: str = None,
                 debug: bool = False):
        self.driver = driver
        if not desc:
            raise KError("元素描述不能为空")
        else:
            self._desc = desc
        self.target_image = image
        self._debug = debug

    def __get__(self, instance, owner):
        if instance is None:
            return None

        self.driver = instance.driver
        return self

    def find(self, timout=3):
        logger.info(f'查找元素: {self._desc}')
        for i in range(3):
            logger.info(f'第{i + 1}次查找:')
            point = self.driver.locate(self.target_image)
            if point is not None:
                x, y = point
                logger.info("查找成功")
                if self._debug is True:
                    file_path = self.driver.screenshot(f'{self._desc}_查找成功')
                    draw_red_by_rect(file_path, (int(x * 2) - 50, int(y * 2) - 50, 100, 100))
                return x, y
            else:
                logger.info("查找失败")
                time.sleep(timout)
        else:
            self.driver.screenshot(f'{self._desc}_查找失败')
            raise KError(f'{self._desc}_查找失败')

    def exists(self, timeout=3):
        logger.info(f"检查 {self._desc} 是否存在")
        result = False
        try:
            _element = self.find(timout=timeout)
            result = True
        except:
            result = False
        finally:
            logger.info(result)
            return result

    def click(self):
        logger.info(f"点击 {self._desc}")
        x, y = self.find()
        self.driver.click(x, y)

    def input(self, text: str):
        logger.info(f"输入 {text}")
        self.click()
        self.driver.input(text)


if __name__ == '__main__':
    pass

