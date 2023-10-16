import subprocess
import time
import pyautogui

from kuto.utils.common import screenshot_util
from kuto.utils.log import logger

"""
@Author: kang.yang
@Date: 2023/9/20 10:38
"""


class WinDriver(object):

    def __init__(self, pkg_name: str = None):
        self.app_name = pkg_name

    @staticmethod
    def get_location():
        """获取鼠标位置坐标"""
        while True:
            time.sleep(3)
            x, y = pyautogui.position()
            print(x, y)

    def start_app(self):
        if self.app_name is None:
            raise KeyError("应用名不能为空")

        logger.info(f'启动应用: {self.app_name}')
        cmd = f"start {self.app_name}"
        subprocess.Popen(cmd, shell=True)

    def stop_app(self):
        if self.app_name is None:
            raise KeyError("应用名不能为空")

        logger.info(f'关闭应用: {self.app_name}')
        cmd = f'taskkill /F /IM "{self.app_name}"'
        subprocess.Popen(cmd, shell=True)

    @staticmethod
    def locate(image_path: str):
        """根据图片获取坐标"""
        try:
            x, y = pyautogui.locateCenterOnScreen(image_path)
            return x, y
        except:
            return None

    @staticmethod
    def is_on_screen(x, y):
        """坐标是否在屏幕中"""
        return pyautogui.onScreen(x, y)

    @staticmethod
    def click(x, y):
        logger.info(f"点击: ({x}, {y})")
        pyautogui.click(x, y)

    @staticmethod
    def input(text: str):
        logger.info(f"输入: {text}")
        pyautogui.write(text)

    @staticmethod
    def enter():
        logger.info("回车")
        pyautogui.press("enter")

    @staticmethod
    def screenshot(file_name=None, position: str = None):
        return screenshot_util(pyautogui, file_name=file_name, position=position)


if __name__ == '__main__':
    WinDriver(pkg_name='calc.exe').get_location()



