import logging
import os
import time
from urllib import parse

# import allure
import allure
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver import (
    ChromeOptions,
    DesiredCapabilities,
    EdgeOptions,
    FirefoxOptions,
)
from selenium.webdriver.chrome.service import Service as cService
from selenium.webdriver.edge.service import Service as eService
from selenium.webdriver.firefox.service import Service as fService
from selenium.webdriver.ie.service import Service as iService
from selenium.webdriver.remote.remote_connection import LOGGER
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager

from kuto.utils.common import screenshot_util
from kuto.utils.log import logger
from kuto.utils.webdriver_manager_extend import ChromeDriverManager


LOGGER.setLevel(logging.WARNING)


def get_selenium_driver(browserName: str, headless: bool = False, timeout: int = 60):
    browser = SeleniumBrowser(browserName, headless, timeout)
    return SeleniumDriver(browser)


class SeleniumBrowser(object):
    """
    根据关键词初始化浏览器操作句柄，
    如'chrome、google chrome、gc'代表chrome浏览器，
    如'firefox、ff'代表火狐浏览器，
    如'internet explorer、ie、IE'代表IE浏览器，
    如'edge'代表edge浏览器，
    如'safari'代表safari浏览器
    """

    def __init__(self, name, headless=False, timeout=60):
        self.name = name
        self.timeout = timeout
        self.headless = headless

    def start(self):
        if self.name == 'Chrome':
            return self.chrome()
        elif self.name == 'Firefox':
            return self.firefox()
        elif self.name == 'Webkit':
            return self.safari()
        else:
            return self.chrome()

    def chrome(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument(
            f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        )
        if self.headless:
            chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(
            options=chrome_options, executable_path=ChromeDriverManager().install()
        )

        driver.set_page_load_timeout(self.timeout)

        return driver

    def firefox(self):
        firefox_options = FirefoxOptions()
        firefox_options.add_argument(
            f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0"
        )
        if self.headless:
            firefox_options.add_argument("--headless")

        driver = webdriver.Firefox(
            options=firefox_options, executable_path=GeckoDriverManager().install()
        )

        driver.set_page_load_timeout(self.timeout)

        return driver

    # @staticmethod
    # def ie():
    #     if IEConfig.command_executor == "":
    #         driver = webdriver.Ie(service=iService(IEDriverManager().install()))
    #     elif IEConfig.command_executor[:4] == "http":
    #         driver = webdriver.Remote(
    #             command_executor=IEConfig.command_executor,
    #             desired_capabilities=DesiredCapabilities.INTERNETEXPLORER.copy(),
    #         )
    #     else:
    #         driver = webdriver.Ie(executable_path=IEConfig.command_executor)
    #
    #     return driver
    #
    # @staticmethod
    # def edge():
    #     if EdgeConfig.options is None:
    #         edge_options = EdgeOptions()
    #     else:
    #         edge_options = EdgeConfig.options
    #
    #     if EdgeConfig.headless is True:
    #         edge_options.headless = True
    #
    #     if EdgeConfig.command_executor == "":
    #         driver = webdriver.Edge(
    #             options=edge_options,
    #             service=eService(EdgeChromiumDriverManager().install()),
    #         )
    #     elif EdgeConfig.command_executor[:4] == "http":
    #         driver = webdriver.Remote(
    #             options=edge_options,
    #             command_executor=EdgeConfig.command_executor,
    #             desired_capabilities=DesiredCapabilities.EDGE.copy(),
    #         )
    #     else:
    #         driver = webdriver.Edge(
    #             options=edge_options, executable_path=EdgeConfig.command_executor
    #         )
    #
    #     return driver

    def safari(self):
        # if (
        #     SafariConfig.command_executor != ""
        #     and SafariConfig.command_executor[:4] == "http"
        # ):
        #     return webdriver.Remote(
        #         command_executor=SafariConfig.command_executor,
        #         desired_capabilities=DesiredCapabilities.SAFARI.copy(),
        #     )

        driver = webdriver.Safari(executable_path="/usr/bin/safaridriver")
        driver.set_page_load_timeout(self.timeout)
        return driver


class SeleniumDriver(object):

    def __init__(self, browser: SeleniumBrowser):
        self.d = browser.start()

    @property
    def page_content(self):
        logger.info('get page content')
        page_source = self.d.page_source
        return page_source

    @property
    def title(self):
        logger.info("get title")
        title = self.d.title
        return title

    @property
    def url(self):
        logger.info("get url")
        url = self.d.current_url
        return url

    @property
    def alert_text(self):
        logger.info("get alert text")
        try:
            alert_text = self.d.switch_to.alert.text
        except NoAlertPresentException:
            logger.info(f'没有出现alert')
            return None
        return alert_text

    def set_page_timeout(self, timeout):
        """设置页面超时时间"""
        self.d.set_page_load_timeout(timeout)

    def set_script_time(self, timeout):
        """设置异步脚本的超时时间"""
        self.d.set_script_timeout(timeout)

    def open_url(self, url=None):
        """访问url"""
        logger.info(f"visit {url}")
        self.d.get(url)

    def add_cookies_and_refresh(self, headers: dict):
        """添加cookie后刷新页面"""
        if headers:
            cookies = [{"name": k, "value": v} for k, v in headers.items()]
            self.add_cookies(cookies)
            self.refresh()

    def back(self):
        logger.info("back")
        self.d.back()

    def screenshot(self, file_name=None, with_time=True, delay=2):
        screenshot_util(self.d, file_name=file_name, with_time=with_time,
                        delay=delay)

    def get_windows(self):
        logger.info(f"get tab list")
        return self.d.window_handles

    def switch_window(self, old_windows):
        logger.info("switch to newest tab")
        current_windows = self.d.window_handles
        newest_window = [window for window in current_windows if window not in old_windows][0]
        self.d.switch_to.window(newest_window)

    def switch_to_frame(self, frame_id):
        logger.info(f"switch to frame {frame_id}")
        self.d.switch_to.frame(frame_id)

    def frame_out(self):
        logger.info("switch frame out")
        self.d.switch_to.default_content()

    def execute_js(self, script, *args):
        logger.info(f"exec js script: \n{script}")
        self.d.execute_script(script, *args)

    def click_elem(self, element):
        logger.info(f"click: {element}")
        self.d.execute_script("arguments[0].click();", element)

    def quit(self):
        logger.info("quit browser")
        self.d.quit()

    def close(self):
        logger.info("close current tab")
        self.d.close()

    def add_cookies(self, cookies: list):
        """添加cookie列表"""
        for cookie in cookies:
            self.d.add_cookie(cookie)

    def get_cookies(self):
        """获取所有cookie"""
        logger.info("get all cookie")
        cookies = self.d.get_cookies()
        logger.info(cookies)
        return cookies

    def refresh(self):
        logger.info(f"refresh page")
        self.d.refresh()

    def accept_alert(self):
        logger.info("alert accept")
        self.d.switch_to.alert.accept()

    def dismiss_alert(self):
        logger.info("alert dismiss")
        self.d.switch_to.alert.dismiss()


if __name__ == '__main__':
    pass


