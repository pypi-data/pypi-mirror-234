from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from kuto.utils.exceptions import KError
from kuto.utils.log import logger
from kuto.web.selenium_driver import SeleniumDriver


class SeleElem:
    """
    通过selenium定位的web元素
    """

    def __init__(self,
                 driver: SeleniumDriver = None,
                 xpath: str = None,
                 css: str = None
                 ):
        """

        @param driver: 浏览器驱动
        @param xpath: 根据xpath进行定位
        @param css: 根据css selector进行定位
        """
        self._driver = driver

        if xpath:
            self.loc = (By.XPATH, xpath)
        if css:
            self.loc = (By.CSS_SELECTOR, css)

    def __get__(self, instance, owner):
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    def _wait(self, timeout=3):
        try:
            WebDriverWait(self._driver.d, timeout=timeout).until(
                EC.visibility_of_element_located(self.loc)
            )
            return True
        except Exception:
            return False

    # def _find_element(self, retry=3, timeout=5):
    #     cur_retry = retry
    #     while not self._wait(timeout=timeout):
    #         if cur_retry > 0:
    #             logger.warning(f"第{retry-cur_retry+1}次重试，查找元素： {self.loc}")
    #             cur_retry -= 1
    #         else:
    #             frame = inspect.currentframe().f_back
    #             caller = inspect.getframeinfo(frame)
    #             logger.warning(
    #                 f"【{caller.function}:{caller.lineno}】Not found element {self.loc}"
    #             )
    #             return None
    #     elements = self._driver.d.find_elements(*self.loc)
    #     return elements

    def _find_element(self, timeout=5):
        logger.info(f'try find {self.loc}')
        if self._wait(timeout):
            return self._driver.d.find_elements(*self.loc)
        else:
            return None

    def get_elements(self, timeout=3):
        elements = self._find_element(timeout=timeout)
        if elements is None:
            raise KError(f"[控件 {self.loc} 定位失败]")
        self._driver.screenshot("loc")
        return elements

    def get_element(self, timeout=3):
        elements = self.get_elements(timeout=timeout)
        return elements[0]

    @property
    def display(self):
        logger.info(f"get is_displayed")
        displayed = self.get_element().is_displayed()
        return displayed

    @property
    def text(self):
        logger.info(f"get text")
        element = self.get_element()
        text = element.text
        return text

    def get_attr(self, attr_name):
        logger.info(f"get {attr_name}")
        value = self.get_element().get_attribute(attr_name)
        return value

    def exists(self, timeout=3):
        logger.info(f"if exists")
        element = self._find_element(timeout=timeout)
        if element is None:
            return False
        return True

    def click(self, timeout=5):
        logger.info(f"click")
        self.get_element(timeout=timeout).click()

    def click_exists(self, timeout=1):
        logger.info(f"click if exists")
        if self.exists(timeout=timeout):
            self.click()

    def set_text(self, text):
        logger.info(f"input text")
        self.get_element().send_keys(text)

    def clear_text(self):
        logger.info(f"clear")
        self.get_element().clear()

    def enter(self):
        logger.info(f"enter")
        self.get_element().send_keys(Keys.ENTER)


if __name__ == '__main__':
    pass





