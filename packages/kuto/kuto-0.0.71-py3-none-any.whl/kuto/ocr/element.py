import time

from kuto.utils.exceptions import KError
from kuto.utils.log import logger
from kuto.ocr.driver import OCRDiscern
from kuto.utils.common import draw_red_by_rect

# 先上下左右分成四块，然后再上下对半分
POSITION = {
    1: "top_left",
    11: "top_left_1",
    12: "top_left_2",
    2: "top_right",
    21: "top_right_1",
    22: "top_right_2",
    3: "bottom_left",
    31: "bottom_left_1",
    32: "bottom_left_2",
    4: "bottom_right",
    41: "bottom_right_1",
    42: "bottom_right_2"
}


class OCRElem(object):
    """ocr识别定位"""

    def __init__(self,
                 driver=None,
                 text: str = None,
                 pos: int = None,
                 grade=0.8,
                 scale: int = None,
                 desc: str = None,
                 debug: bool = False):
        """
        @param driver:
        @param text:
        @param pos: 把图片分成八块，具体定义见上POSITION
        @param grade: 置信度，最大1，越高代表准确率越高
        @param debug: 是否调试
        """
        self.driver = driver
        self.text = text
        self._position = pos
        if pos is not None:
            self._position = POSITION[pos]
        self._grade = grade
        self._debug = debug
        self._scale = scale
        self._desc = desc
        if self._desc is None:
            raise KError("元素描述不能为空")

    def __get__(self, instance, owner):
        if instance is None:
            return None

        self.driver = instance.driver
        return self

    def find_element(self, retry=3, timeout=1):
        logger.info(f"开始查找元素: {self.text}")
        for i in range(retry):
            time.sleep(timeout)
            logger.info(f"第{i+1}次识别")
            info = self.driver.screenshot(self._desc + f"_第{i+1}次识别",
                                          position=self._position)
            if self._position is not None:
                image_path = info.get("path")
            else:
                image_path = info
            res = OCRDiscern(image_path, grade=self._grade).get_coordinate(self.text)
            if isinstance(res, tuple):
                x, y = res
                if self._position is not None:
                    logger.debug(self._position)
                    width = info.get("width")
                    height = info.get("height")
                    cut_height = info.get("cut_height")

                    if 'top_right' in self._position:
                        x = width / 2 + x
                        if self._position == "top_right_2":
                            y = y + cut_height
                    elif 'top_left' in self._position:
                        if self._position == 'top_left_2':
                            y = y + cut_height
                    elif 'bottom_left' in self._position:
                        y = height / 2 + y
                        if self._position == "bottom_left_2":
                            y = y + cut_height
                    elif 'bottom_right' in self._position:
                        x = width / 2 + x
                        y = height / 2 + y
                        if self._position == "bottom_right_2":
                            y = y + cut_height

                if self._scale is not None:
                    """iphone的scale是3"""
                    x, y = int(x/self._scale), int(y/self._scale)
                logger.info(f'识别坐标为: ({x}, {y})')
                if self._debug is True:
                    file_path = self.driver.screenshot(f'ocr识别定位成功-{self._desc}')
                    if self._scale is not None:
                        _x, _y = x * self._scale, y * self._scale
                        draw_red_by_rect(file_path, (int(_x) - 100, int(_y) - 100, 200, 200))
                    draw_red_by_rect(file_path, (int(x) - 100, int(y) - 100, 200, 200))
                return x, y

        else:
            self.driver.screenshot(f'ocr识别定位失败-{self._desc}')
            raise Exception('通过OCR未识别指定文字或置信度过低，无法进行点击操作！')

    def exists(self, timeout=1):
        logger.info(f'ocr识别文本: {self.text} 是否存在')
        try:
            self.find_element(timeout=timeout)
        except Exception as e:
            logger.debug(str(e))
            return False
        else:
            return True

    def click(self, retry=3, timeout=3):
        logger.info(f'ocr点击文本: {self.text}')
        x, y = self.find_element(retry=retry, timeout=timeout)
        self.driver.click(x, y)
        logger.info("点击完成")


if __name__ == '__main__':
    pass



