import os
import re
import subprocess

import requests
import six

from kuto.utils.log import logger
from kuto.utils.exceptions import KError


class SibUtil:
    """sib操作
    本地需要部署sib环境，参考：https://github.com/SonicCloudOrg/sonic-ios-bridge
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port

    @staticmethod
    def get_current_devices():
        """
        获取当前设备列表
        @return:
        """
        cmd = 'sib devices'
        output = os.popen(cmd).read()
        print(output)
        device_list = [item.split(' ')[0] for item in output.split('\n') if item]
        if device_list:
            return device_list
        else:
            raise KError(msg=f"无已连接设备")

    def connect(self):
        """
        连接远程设备
        @return:
        """
        cmd = f'sib remote connect --host {self.host} --port {self.port}'
        output = subprocess.getoutput(cmd)
        print(output)
        if 'succeeded' in output:
            logger.info('连接成功')
            return self.get_current_devices()[-1]
        else:
            raise KError(f'连接失败: \n{output}')

    def disconnect(self):
        """
        断开远程连接
        @return:
        """
        cmd = f'sib remote disconnect --host {self.host} --port {self.port}'
        logger.info(cmd)
        output = subprocess.getoutput(cmd)
        print(output)
        logger.info(output)

    @staticmethod
    def download_apk(src):
        """下载安装包"""
        if isinstance(src, six.string_types):
            if re.match(r"^https?://", src):
                logger.info(f'下载中: {src}')
                file_path = os.path.join(os.getcwd(), src.split('/')[-1])
                r = requests.get(src, stream=True)
                if r.status_code != 200:
                    raise IOError(
                        "Request URL {!r} status_code {}".format(src, r.status_code))
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                logger.info(f'下载成功: {file_path}')
                return file_path
            elif os.path.isfile(src):
                return src
            else:
                raise IOError("static {!r} not found".format(src))

    @staticmethod
    def uninstall_app(device_id: str, pkg_name: str):
        """
        卸载应用
        @param device_id:
        @param pkg_name:
        @return:
        """
        # 使用sib命令安装应用
        cmd = f"sib app uninstall -u {device_id} -b {pkg_name}"
        logger.info(f"卸载应用: {pkg_name}")
        output = subprocess.getoutput(cmd)
        print(output)
        if "successful" in output.split()[-1]:
            logger.info(f"{device_id} 卸载应用 {pkg_name} 成功")
            return
        else:
            logger.info(f"{device_id} 卸载应用 {pkg_name} 失败，因为 {output}")

    def install_app(self, device_id: str, ipa_url: str):
        """
        安装app
        @return:
        """
        # 下载应用
        ipa_path = self.download_apk(ipa_url)

        # 使用sib命令安装应用
        cmd = f"sib app install -u {device_id} -p {ipa_path}"
        logger.info(f"安装应用: {ipa_url}")
        output = subprocess.getoutput(cmd)
        print(output)
        if "successful" in output.split()[-1]:
            logger.info(f"{device_id} 安装应用 {ipa_url} 成功")
            return
        else:
            logger.info(f"{device_id} 安装应用 {ipa_url} 失败，因为{output}")

        # 删除下载的安装包
        if 'http' in ipa_url:
            os.remove(ipa_path)


if __name__ == '__main__':
    sib = SibUtil('172.16.1.216', '51385')
    # device_id = sib.connect()
    pkg_name = 'com.qizhidao.company'
    # ipa_url = 'http://172.16.5.225:8081/AppUpdateTest/pre_qizhiyun_client_4.3.2.ipa'
    # sib.uninstall_app(device_id, pkg_name)
    # sib.disconnect()
    print(sib.get_current_devices())








