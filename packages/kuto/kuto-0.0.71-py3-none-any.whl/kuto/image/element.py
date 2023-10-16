import time

from kuto.utils.exceptions import KError
from kuto.utils.log import logger
from kuto.image.driver import ImageDiscern
from kuto.utils.common import draw_red_by_rect


class ImageElem(object):
    """图像识别定位"""

    def __init__(self,
                 driver=None,
                 desc: str = None,
                 file: str = None,
                 scale: int = None,
                 grade=0.9,
                 gauss_num=111,
                 debug: bool = False):
        self.driver = driver
        if not desc:
            raise KError("元素描述不能为空")
        else:
            self._desc = desc
        self.target_image = file
        self._debug = debug
        self._scale = scale
        self._grade = grade
        self._gauss_num = gauss_num

    def __get__(self, instance, owner):
        if instance is None:
            return None

        self.driver = instance.driver
        return self

    def exists(self, timeout=1):
        logger.info(f'图像识别判断: {self._desc} 是否存在')
        time.sleep(timeout)
        source_image = self.driver.screenshot(self._desc + "_识别中")
        res = ImageDiscern(self.target_image, source_image, self._grade, self._gauss_num).get_coordinate()
        logger.debug(res)
        if isinstance(res, tuple):
            return True
        else:
            return False

    def click(self, retry=3, timeout=3):
        logger.info(f'图像识别点击图片: {self._desc}')
        for i in range(retry):
            time.sleep(timeout)
            logger.info(f'第{i + 1}次查找:')
            source_image = self.driver.screenshot(self._desc)
            res = ImageDiscern(self.target_image, source_image, self._grade, self._gauss_num).get_coordinate()
            if isinstance(res, tuple):
                logger.info(f'识别坐标为: {res}')
                x, y = res[0], res[1]
                if self._scale is not None:
                    """iphone的scale是3"""
                    x, y = int(x/self._scale), int(y/self._scale)
                if self._debug is True:
                    file_path = self.driver.screenshot(f'图像识别定位成功-{self._desc}')
                    if self._scale is not None:
                        _x, _y = x * self._scale, y * self._scale
                        draw_red_by_rect(file_path, (int(_x) - 100, int(_y) - 100, 200, 200))
                    draw_red_by_rect(file_path, (int(x) - 100, int(y) - 100, 200, 200))
                self.driver.click(x, y)
                return
        else:
            self.driver.screenshot(f'图像识别定位失败-{self._desc}')
            raise Exception('未识别到图片，无法进行点击')


if __name__ == '__main__':
    pass


