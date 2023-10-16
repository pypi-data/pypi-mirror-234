"""
@Author: kang.yang
@Date: 2023/9/20 11:21
"""
from kuto.utils.config import config
from kuto.utils.exceptions import KError
from urllib import parse


class Page(object):
    """页面基类，用于pom模式封装"""

    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str = None):
        if getattr(self, 'url', None) is None:
            if url is None:
                raise KError('url不能为空')
        else:
            url = getattr(self, 'url')

        if not url.startswith('http'):
            host = config.get_common('base_url')
            if host is not None:
                url = parse.urljoin(host, url)
            else:
                raise KError('host不能为空')

        if getattr(self.driver, 'open_url', None) is not None:
            self.driver.open_url(url)
        else:
            raise KError('driver没有open_url方法')



