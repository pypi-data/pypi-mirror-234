import click
import subprocess
# import argparse

# from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
# from kuto.utils.webdriver_manager_extend import ChromeDriverManager
#
# from kuto.utils.log import logger
# # from kuto.scaffold import create_scaffold
from kuto import __version__
from kuto.scaffold import create_scaffold


@click.command()
@click.version_option(version=__version__, help="Show version.")
@click.option("-i", "--install", is_flag=True, help="Install the browser driver.")
# @click.option("-p", "--platform", type=str, default=None, help="Create demo by platform, api、ios、android、web")
# 老是变，等最后定下来再搞，目前也没啥用
def main(install, platform):
    """App、Web、Api auto tests framework"""
    if install:
        subprocess.run(["playwright", "install"])

    # if platform:
    #     create_scaffold(platform)

    # parser = argparse.ArgumentParser(description=__description__)
    # parser.add_argument(
    #     "-v", "--version", dest="version", action="store_true", help="版本号"
    # )
    # parser.add_argument(
    #     "-p", "--platform", dest="platform", help="所属平台，android、ios、web、api，用于创建demo"
    # )
    # parser.add_argument(
    #     "-i", "--install", dest="install", help="浏览器驱动名称，chrome、firefox、edge，用于安装浏览器驱动"
    # )

    # args = parser.parse_args()
    # version = args.version
    # platform = args.platform
    # install = args.install

    # if version:
    #     print(__version__)
    #     return 0
    # if platform:
    #     create_scaffold(platform)
    #     return 0
    # if install:
    #     install_driver(install)
    #     return 0


# def install_driver(browser: str) -> None:
#     """
#     Download and install the browser driver
#     :param browser: The Driver to download. Pass as `chrome/firefox/ie/edge`. Default Chrome.
#     :return:
#     """
#
#     if browser == "chrome":
#         driver_path = ChromeDriverManager().install()
#         logger.info(f"Chrome Driver[==>] {driver_path}")
#     elif browser == "firefox":
#         driver_path = GeckoDriverManager().install()
#         logger.info(f"Firefox Driver[==>] {driver_path}")
#     elif browser == "ie":
#         driver_path = IEDriverManager().install()
#         logger.info(f"IE Driver[==>] {driver_path}")
#     elif browser == "edge":
#         driver_path = EdgeChromiumDriverManager().install()
#         logger.info(f"Edge Driver[==>] {driver_path}")
#     else:
#         raise NameError(f"Not found '{browser}' browser driver.")
