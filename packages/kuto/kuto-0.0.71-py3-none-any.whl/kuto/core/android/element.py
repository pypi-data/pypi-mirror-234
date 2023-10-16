import typing

from uiautomator2 import UiObject
from uiautomator2.xpath import XPathSelector

from kuto.android import AndroidDriver
from kuto.utils.exceptions import KError
from kuto.utils.log import logger
from kuto.utils.common import calculate_time, draw_red_by_coordinate


class AdrElem(object):
    """
    安卓元素定义
    """

    def __init__(self,
                 AdrDriver: AndroidDriver = None,
                 desc: str = None,
                 rid: str = None,
                 className: str = None,
                 text: str = None,
                 textCont: str = None,
                 xpath: str = None,
                 index: int = None,
                 debug: bool = False):
        """
        @param AdrDriver: 安卓驱动，必填
        @param desc: 元素描述，必填
        @param rid: resourceId定位
        @param className: className定位
        @param text: text定位
        @param textCont: text包含
        @param xpath: xpath定位
        @param index: 定位出多个元素时，指定索引，从0开始
        @param debug: 是否调试
        """
        self._driver = AdrDriver
        if not desc:
            raise KError("元素描述不能为空")
        else:
            self._desc = desc

        self._kwargs = {}
        if rid is not None:
            self._kwargs["resourceId"] = rid
        if className is not None:
            self._kwargs["className"] = className
        if text is not None:
            self._kwargs["text"] = text
        if textCont is not None:
            self._kwargs["textContains"] = textCont
        if xpath:
            self._kwargs["xpath"] = xpath
        if index is not None:
            self._kwargs["instance"] = index

        self._xpath = xpath
        self._debug = debug

    def __get__(self, instance, owner):
        """po模式中element初始化不需要带driver的关键"""
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    @calculate_time
    def find(self, timeout=10, watch=None):
        """
        增加截图的方法
        @param timeout: 每次查找时间
        @param watch: 增加弹窗检测，定位方式列表，用text定位
        watch为True时，使用内置库
            when("继续使用")
            when("移入管控").when("取消")
            when("^立即(下载|更新)").when("取消")
            when("同意")
            when("^(好的|确定)")
            when("继续安装")
            when("安装")
            when("Agree")
            when("ALLOW")
        watch为list时，使用内置库+watch
        @return:
        """
        rid = self._kwargs.get("resourceId", None)
        if rid is not None:
            pkg_name = self._driver.pkg_name
            if pkg_name not in rid:
                if "id/" not in rid:
                    self._kwargs["resourceId"] = pkg_name + ":id/" + rid
                else:
                    self._kwargs["resourceId"] = pkg_name + ":" + rid

        def _find():
            if self._xpath is not None:
                logger.info(f'查找控件: xpath={self._xpath}')
            else:
                logger.info(f'查找控件: {self._kwargs}')
            _element = self._driver.d.xpath(self._xpath) if \
                self._xpath is not None else self._driver.d(**self._kwargs)

            if _element.wait(timeout=timeout):
                logger.info(f"查找成功")
                if self._debug is True:
                    file_path = self._driver.screenshot(self._desc + "_查找成功")
                    logger.debug(file_path)
                    draw_red_by_coordinate(file_path, _element.bounds())
                return _element
            else:
                logger.info(f"查找失败")
                self._driver.screenshot(self._desc + "_查找失败")
                raise KError(f"控件 {self._kwargs} 查找失败")

        if watch:
            logger.info("开启弹窗检测")
            if isinstance(watch, list):
                with self._driver.d.watch_context(builtin=True) as ctx:
                    for text in watch:
                        ctx.when(text).click()
                    ctx.wait_stable()
                    logger.info("结束检测")
                    return _find()
            else:
                with self._driver.d.watch_context(builtin=True) as ctx:
                    ctx.wait_stable()
                    logger.info("结束检测")
                    return _find()
        else:
            return _find()

    @property
    def text(self):
        logger.info(f"获取 {self._desc} 文本属性")
        _elem = self.find(timeout=3)
        if isinstance(_elem, XPathSelector):
            elems = _elem.all()
        else:
            elems = list(_elem)
        text = []
        for elem in elems:
            text.append(elem.get_text())
        logger.info(text)
        return text

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

    @staticmethod
    def _adapt_center(e: typing.Union[UiObject, XPathSelector],
                      offset=(0.5, 0.5)):
        """
        修正控件中心坐标
        """
        if isinstance(e, UiObject):
            return e.center(offset=offset)
        else:
            return e.offset(offset[0], offset[1])

    def click(self, timeout=5, watch=None):
        logger.info(f"点击 {self._desc}")
        element = self.find(timeout=timeout, watch=watch)
        # 这种方式经常点击不成功，感觉是页面刷新有影响
        # element.click()
        x, y = self._adapt_center(element)
        self._driver.d.click(x, y)

    def click_exists(self, timeout=3, watch=None):
        logger.info(f"{self._desc} 存在才点击")
        if self.exists(timeout=timeout):
            self.click(watch=watch)

    def input(self, text, watch=None):
        logger.info(f"输入文本: {text}")
        self.find(watch=watch).set_text(text)

    def input_exists(self, text: str, timeout=3, watch=None):
        logger.info(f"{self._desc} 存在才输入: {text}")
        if self.exists(timeout=timeout):
            self.input(text, watch=watch)

    def input_pwd(self, text, watch=None):
        """密码输入框输入有时候用input输入不了"""
        logger.info(f"输入密码: {text}")
        self.find(watch=watch).click()
        self._driver.d(focused=True).set_text(text)

    def clear(self, watch=None):
        logger.info("清空输入框")
        self.find(watch=watch).clear_text()

    def assert_exists(self, timeout=3):
        logger.info(f"断言 {self._desc} 存在")
        status = self.exists(timeout=timeout)
        assert status, "控件不存在"

    def assert_text(self, text, timeout=3, watch=None):
        logger.info(f"断言 {self._desc} 文本属性包括: {text}")
        self.find(timeout=timeout, watch=watch)
        _text = self.text
        assert text in _text, f"文本属性 {_text} 不包含 {text}"


if __name__ == '__main__':
    driver = AndroidDriver(
        device_id="UJK0220521066836",
        pkg_name="com.qizhidao.clientapp"
    )
    driver.start_app()
    AdrElem(driver, rid='com.qizhidao.clientapp:id/bottom_btn').click()
    AdrElem(driver, text='我的', debug=True).click()






