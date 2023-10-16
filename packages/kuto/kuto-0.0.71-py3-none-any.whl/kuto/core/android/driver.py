import os
import re
import time
import subprocess
import requests
import six
import uiautomator2 as u2

from kuto.utils.log import logger
from kuto.utils.common import screenshot_util
from kuto.utils.exceptions import KError
from kuto.android.common import get_connected_adr_devices


class AndroidDriver(object):

    def __init__(self, device_id=None, pkg_name=None):
        logger.info("初始化安卓驱动")
        self.pkg_name = pkg_name
        if not self.pkg_name:
            raise KError('应用包名不能为空')
        self.device_id = device_id
        if not self.device_id:
            # 未传入设备id时，获取已连接设备
            self.device_id = get_connected_adr_devices()[0]

        self.d = u2.connect(self.device_id)

        if not self.d.alive:
            """判断uiautomator服务是否正常运行，否则重启它"""
            logger.info("uiautomator异常，进行重启！！！")
            self.d.healthcheck()
        else:
            logger.info("uiautomator已就绪")

    @property
    def app_info(self):
        logger.info("获取应用信息")
        info = self.d.app_info(self.pkg_name)
        logger.info(info)
        return info

    @property
    def device_info(self):
        logger.info(f"获取设备信息")
        info = self.d.device_info
        logger.info(info)
        return info

    @property
    def page_content(self):
        logger.info("获取页面xml")
        info = self.d.dump_hierarchy()
        logger.info(info)
        return info

    def assert_act(self, activity_name: str, timeout=5):
        logger.info(f"断言 activity 等于 {activity_name}")
        assert self.d.wait_activity(activity_name, timeout=timeout)

    def uninstall_app(self):
        logger.info(f"卸载应用")
        self.d.app_uninstall(self.pkg_name)

    @staticmethod
    def download_apk(src):
        """下载安装包"""
        start = time.time()
        if isinstance(src, six.string_types):
            if re.match(r"^https?://", src):
                logger.info(f'下载中...')
                file_path = os.path.join(os.getcwd(), src.split('/')[-1])
                r = requests.get(src, stream=True)
                if r.status_code != 200:
                    raise IOError(
                        "Request URL {!r} status_code {}".format(src, r.status_code))
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                end = time.time()
                logger.info(f'下载成功: {file_path}，耗时: {end - start}s')
                return file_path
            elif os.path.isfile(src):
                return src
            else:
                raise IOError("static {!r} not found".format(src))

    def install_app(self, apk_path, auth=True, new=True, helper: list = None):
        """
        安装应用，push改成adb命令之后暂时无法支持远程手机调用
        @param apk_path: 安装包链接，支持本地路径以及http路径
        @param auth: 是否进行授权
        @param new: 是否先卸载再安装
        @param helper：install命令后的各品牌机型适配
        [
            ["assert", {"text": "未发现风险"}],
            ["click", {"text": "继续安装"}],
            ["click", {"text": "完成"}],
            ["input", {"resourceId": "xxx"}, "yyy"]
        ]
        """
        start = time.time()
        logger.info(f"安装应用: {apk_path}")
        # 卸载
        if new is True:
            self.uninstall_app()

        # 下载
        try:
            source = self.download_apk(apk_path)
        except:
            raise KeyError("下载apk失败")

        # 安装
        try:
            cmd_list = ['adb', 'install', "-r", "-t", source]
            if auth is True:
                cmd_list.insert(4, '-g')
            logger.debug(f"{' '.join(cmd_list)}")
            process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if helper is None:
                # 等待子进程执行完成
                process.wait()
        except:
            raise KeyError("adb安装失败")

        # 各品牌机型适配
        try:
            if helper is not None:
                for step in helper:
                    method = step[0]
                    loc = step[1]
                    if method == "click":
                        self.d(**loc).click()
                    elif method == "assert":
                        assert self.d(**loc).wait(timeout=10)
                    elif method == "input":
                        content = step[2]
                        self.d(**loc).send_keys(content)
                    else:
                        raise KeyError("不支持的方法")
        except:
            raise KeyError("安装过程处理失败")

        # 删除下载的安装包
        if 'http' in apk_path:
            os.remove(source)

        end = time.time()
        logger.info(f'安装成功，耗时: {end - start}s')

    def start_app(self, stop=True):
        """启动应用
        @param stop: 是否先关闭应用再启动
        """
        logger.info(f"启动应用")
        self.d.app_start(self.pkg_name, stop=stop, use_monkey=True)

    def stop_app(self):
        logger.info("关闭应用")
        self.d.app_stop(self.pkg_name)

    def screenshot(self, file_name=None, position: str = None):
        return screenshot_util(self.d, file_name=file_name, position=position)

    def back(self):
        logger.info("返回上一页")
        self.d.press('back')

    def click(self, x, y):
        logger.info(f"点击坐标: {x}, {y}")
        self.d.click(x, y)

    def click_alerts(self, alert_list: list):
        logger.info(f"点击弹窗: {alert_list}")
        with self.d.watch_context() as ctx:
            for alert in alert_list:
                ctx.when(alert).click()
            ctx.wait_stable()

    def swipe(self, direction: str = None):
        logger.info(f"swipe {direction}")
        key_range = ["left", "right", "up", "down"]
        if direction not in key_range:
            raise KeyError(f"direction取值只能是 {key_range} 其中一个")
        self.d.swipe_ext(direction)


if __name__ == '__main__':
    driver1 = AndroidDriver(
        device_id="UJK0220521066836",
        pkg_name="com.qizhidao.clientapp"
    )
    # helper = [
    #     {"method": "assert", "loc": "未发现风险"},
    #     {"method": "click", "loc": "继续安装"},
    #     {"method": "click", "loc": "完成"}
    # ]
    helper1 = [
        ["assert", {"text": "未发现风险"}],
        ["click", {"text": "继续安装"}],
        ["click", {"text": "完成"}],
    ]
    driver1.install_app(
        apk_path="http://maven.qizhidao.net:8081/repository/packages-host/qzd/qizhidao_app_android/dev-work/jenkins_771/app_qzd_v4.4.2_80403001_2023-07-26_arm64-v8a_pre_release.apk")
    driver1.start_app()














