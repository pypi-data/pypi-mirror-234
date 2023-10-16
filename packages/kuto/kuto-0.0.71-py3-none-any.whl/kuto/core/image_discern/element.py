import time

from kuto.ios.driver import IosDriver
from kuto.utils.exceptions import KError
from kuto.utils.log import logger
from kuto.core.image_discern.driver import ImageDiscern
from kuto.utils.common import draw_red_by_rect


class ImageElem(object):
    """图像识别定位"""

    def __init__(self,
                 driver=None,
                 desc: str = None,
                 image: str = None,
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

    def exists(self, retry=3, timeout=3, grade=0.9, gauss_num=111):
        logger.info(f'图像识别判断: {self._desc} 是否存在')
        time.sleep(3)
        for i in range(retry):
            logger.info(f'第{i + 1}次查找:')
            source_image = self.driver.screenshot(self._desc)
            res = ImageDiscern(self.target_image, source_image, grade, gauss_num).get_coordinate()
            logger.debug(res)
            if isinstance(res, tuple):
                return True
            time.sleep(timeout)
        else:
            self.driver.screenshot(f'图像识别定位失败-{self._desc}')
            return False

    def click(self, retry=3, timeout=3, grade=0.9, gauss_num=111):
        logger.info(f'图像识别点击图片: {self._desc}')
        time.sleep(3)
        for i in range(retry):
            logger.info(f'第{i + 1}次查找:')
            source_image = self.driver.screenshot(self._desc)
            res = ImageDiscern(self.target_image, source_image, grade, gauss_num).get_coordinate()
            if isinstance(res, tuple):
                logger.info(f'识别坐标为: {res}')
                x, y = res[0], res[1]
                if isinstance(self.driver, IosDriver):
                    x, y = int(x/self.driver.d.scale), int(y/self.driver.d.scale)
                if self._debug is True:
                    file_path = self.driver.screenshot(f'图像识别定位成功-{self._desc}')
                    draw_red_by_rect(file_path, (int(x) - 100, int(y) - 100, 200, 200))
                self.driver.click(x, y)
                return
            time.sleep(timeout)
        else:
            self.driver.screenshot(f'图像识别定位失败-{self._desc}')
            raise Exception('未识别到图片，无法进行点击')


if __name__ == '__main__':
    from kuto.android import AndroidDriver

    driver = AndroidDriver(
        device_id='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp'
    )

