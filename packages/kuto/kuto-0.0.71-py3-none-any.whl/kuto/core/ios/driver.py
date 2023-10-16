import shutil
import subprocess
import time
import wda

from kuto.utils.exceptions import KError
from kuto.utils.log import logger
from kuto.utils.common import screenshot_util
from kuto.ios.common import TideviceUtil, get_connected_ios_devices


def _start_wda_xctest(udid: str, port, wda_bundle_id=None):
    xctool_path = shutil.which("tidevice")
    args = []
    if udid:
        args.extend(["-u", udid])
    args.append("wdaproxy")
    args.extend(["--port", str(port)])
    if wda_bundle_id is not None:
        args.extend(["-B", wda_bundle_id])
    p = subprocess.Popen([xctool_path] + args)
    time.sleep(3)
    if p.poll() is not None:
        raise KError("wda启动失败，可能是手机未连接")


class IosDriver(object):

    def __init__(self, device_id: str = None, pkg_name: str = None):
        """device_id可以是udid，也可以是wda服务url"""
        logger.info("初始化ios驱动")
        if not pkg_name:
            raise KError('应用包名不能为空')
        self.pkg_name = pkg_name

        if device_id is None:
            self.device_id = get_connected_ios_devices()[0]
            self.port = self.device_id.split("-")[0][-4:]
            self.wda_url = f"http://localhost:{self.port}"
        else:
            self.device_id = device_id
            if 'http' in self.device_id:
                self.wda_url = self.device_id
            else:
                self.port = self.device_id.split("-")[0][-4:]
                self.wda_url = f"http://localhost:{self.port}"

        self.d = wda.Client(self.wda_url)

        # check if wda is ready
        if self.d.is_ready():
            logger.info('wda已就绪')
        else:
            if 'http' in self.device_id:
                raise KError("wda异常，请确认服务已正常启动！！！")
            else:
                logger.info('wda未就绪, 现在启动')
                _start_wda_xctest(self.device_id, port=self.port)
                if self.d.is_ready():
                    logger.info('wda启动成功')
                else:
                    raise KError('wda启动失败，可能是WebDriverAgent APP端证书失效!')

    @property
    def device_info(self):
        logger.info("获取设备信息")
        info = self.d.device_info()
        logger.info(info)
        return info

    @property
    def current_app(self):
        logger.info("获取当前应用")
        info = self.d.app_current()
        logger.info(info)
        return info

    @property
    def page_content(self):
        logger.info('获取页面xml内容')
        page_source = self.d.source(accessible=False)
        logger.info(page_source)
        return page_source

    def install_app(self, ipa_url, new=True):
        """安装应用
        @param ipa_url: ipa链接
        @param new: 是否先卸载
        @return:
        """
        logger.info(f"安装应用: {ipa_url}")
        if new is True:
            self.uninstall_app()

        TideviceUtil.install_app(self.device_id, ipa_url)

    def uninstall_app(self):
        logger.info(f"卸载应用: {self.pkg_name}")
        TideviceUtil.uninstall_app(self.device_id, self.pkg_name)

    def start_app(self, stop=True):
        """启动应用
        @param stop: 是否先停止应用
        """
        logger.info(f"启动应用: {self.pkg_name}")
        if stop is True:
            self.d.app_terminate(self.pkg_name)
        self.d.app_start(self.pkg_name)

    def stop_app(self):
        logger.info(f"停止应用: {self.pkg_name}")
        self.d.app_terminate(self.pkg_name)

    def back(self):
        """返回上一页"""
        logger.info("返回上一页")
        time.sleep(1)
        self.d.swipe(0, 100, 100, 100)

    def click(self, x, y):
        logger.info(f"点击坐标: {x}, {y}")
        self.d.click(x, y)

    def screenshot(self, file_name=None, position=None):
        return screenshot_util(self.d, file_name=file_name, position=position)

    def click_alerts(self, alert_list: list):
        """点击弹窗"""
        logger.info(f"点击弹窗: {alert_list}")
        try:
            self.d.alert.click(alert_list)
        except:
            pass

    def swipe(self, direction: str = None):
        logger.info(f"swipe {direction}")
        key_range = ["left", "right", "up", "down"]
        if direction not in key_range:
            raise KeyError(f"direction取值只能是 {key_range} 其中一个")
        if direction == "left":
            self.d.swipe_left()
        elif direction == "right":
            self.d.swipe_right()
        elif direction == "up":
            self.d.swipe_up()
        elif direction == "down":
            self.d.swipe_down()


if __name__ == '__main__':
    driver1 = IosDriver(
        device_id="00008101-000E646A3C29003A",
        pkg_name="com.qizhidao.company"
    )
    driver1.start_app()









