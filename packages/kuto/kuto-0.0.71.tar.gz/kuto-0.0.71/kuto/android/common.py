"""
@Author: kang.yang
@Date: 2023/9/7 17:03
"""
import os

from kuto.utils.exceptions import KError
from kuto.utils.log import logger


def get_connected():
    """获取当前连接的手机列表"""
    cmd = 'adb devices'
    output = os.popen(cmd).read()
    device_list = [item.split('\t')[0] for item in output.split('\n') if item.endswith('device')]
    if len(device_list) > 0:
        logger.info(f"已连接设备列表: {device_list}")
        return device_list
    else:
        raise KError(msg=f"无已连接设备")
