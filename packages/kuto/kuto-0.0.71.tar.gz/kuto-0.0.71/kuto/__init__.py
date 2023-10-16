from allure import *
from requests_toolbelt import \
    MultipartEncoder as FormEncoder
from kuto.api.case import Case
from kuto.page import Page
from kuto.running.runner import main
from kuto.utils.config import config
from kuto.utils.log import logger
from kuto.utils.pytest_util import \
    depend, order, data, file_data


__version__ = "0.0.71"
__description__ = "全平台自动化测试框架"
