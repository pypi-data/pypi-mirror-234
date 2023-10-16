import os
import subprocess

from kuto.utils.log import logger
from kuto.utils.exceptions import KError


def get_connected_ios_devices():
    """获取当前连接的设备列表"""
    cmd = 'tidevice list'
    output = os.popen(cmd).read()
    device_list = [item.split(' ')[0] for item in output.split('\n') if item]
    if len(device_list) > 0:
        logger.info(f"已连接设备列表: {device_list}")
        return device_list
    else:
        raise KError(msg=f"无已连接设备")


class TideviceUtil:
    """
    tidevice常用功能的封装
    """

    @staticmethod
    def uninstall_app(device_id=None, pkg_name=None):
        """卸载应用"""
        cmd = f"tidevice -u {device_id} uninstall {pkg_name}"
        logger.info(f"卸载应用: {pkg_name}")
        output = subprocess.getoutput(cmd)
        if "Complete" in output.split()[-1]:
            logger.info(f"{device_id} 卸载应用{pkg_name} 成功")
            return
        else:
            logger.info(f"{device_id} 卸载应用{pkg_name}失败，因为{output}")

    @staticmethod
    def install_app(device_id=None, ipa_url=None):
        """安装应用
        """
        cmd = f"tidevice -u {device_id} install {ipa_url}"
        logger.info(f"安装应用: {ipa_url}")
        output = subprocess.getoutput(cmd)
        if "Complete" in output.split()[-1]:
            logger.info(f"{device_id} 安装应用{ipa_url} 成功")
            return
        else:
            logger.info(f"{device_id} 安装应用{ipa_url}失败，因为{output}")


