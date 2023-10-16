"""
@Author: kang.yang
@Date: 2023/8/1 18:21
"""
import platform
import re
import cv2
import time
import allure
import functools
import os
import random
import socket

from kuto.utils.log import logger


def draw_red_by_rect(image_path: str, rect: tuple):
    """x_top_left, y_top_left, width, height"""
    # 读取图像
    image = cv2.imread(image_path)

    # 定义标记范围的坐标
    x, y, w, h = rect

    # 在图像上绘制矩形
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 保存标记后的图像
    cv2.imwrite(image_path, image)


def draw_red_by_coordinate(image_path: str, rect: tuple):
    """x_top_left, y_top_left, x_bottom_right, y_bottom_right"""
    # 读取图像
    image = cv2.imread(image_path)

    # 定义标记范围的坐标
    x, y, x1, y1 = rect

    # 在图像上绘制矩形
    cv2.rectangle(image, (x, y), (x1, y1), (0, 0, 255), 2)

    # 保存标记后的图像
    cv2.imwrite(image_path, image)


def is_port_in_use(port: int) -> bool:
    """判断端口是否已占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def get_free_port():
    """获取空闲端口"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        try:
            return s.getsockname()[1]
        finally:
            s.close()
    except OSError:
        # bind 0 will fail on Manjaro, fallback to random port
        # https://github.com/openatx/adbutils/issues/85
        for _ in range(20):
            port = random.randint(10000, 20000)
            if not is_port_in_use(port):
                return port
        raise RuntimeError("No free port found")


def cut_half(image, position):
    """把图片分成上下两半"""
    if position == "up":
        return image[:image.shape[0] // 2, :]
    elif position == "down":
        return image[image.shape[0] // 2:, :]
    else:
        raise KeyError("position传值错误")


def cut_by_position(image_path: str, position: str):
    """把图片按左上、左下、右上、右下进行分割"""
    logger.info(position)
    # 读取图像
    logger.info("分割图片")
    start = time.time()
    image = cv2.imread(image_path)
    # 获取图像的宽度和高度
    height, width, _ = image.shape
    logger.debug(f'{height}, {width}')
    # 计算每个切割区域的宽度和高度
    sub_width = width // 2
    sub_height = height // 2
    # 切割图像成上下左右四个等份
    if "top_left" in position:
        image_content = image[0:sub_height, 0:sub_width]
        if position == "top_left_1":
            image_content = cut_half(image_content, "up")
        elif position == "top_left_2":
            image_content = cut_half(image_content, "down")
    elif "top_right" in position:
        image_content = image[0:sub_height, sub_width:width]
        if position == "top_right_1":
            image_content = cut_half(image_content, "up")
        elif position == "top_right_2":
            image_content = cut_half(image_content, "down")
    elif "bottom_left" in position:
        image_content = image[sub_height:height, 0:sub_width]
        if position == "bottom_left_1":
            image_content = cut_half(image_content, "up")
        elif position == "bottom_left_2":
            image_content = cut_half(image_content, "down")
    elif "bottom_right" in position:
        image_content = image[sub_height:height, sub_width:width]
        if position == "bottom_right_1":
            image_content = cut_half(image_content, "up")
        elif position == "bottom_right_2":
            image_content = cut_half(image_content, "down")
    else:
        raise KeyError(f"position传值错误 all: {position}")

    new_path = f"{image_path.split('.')[0]}_{position}.{image_path.split('.')[1]}"
    logger.debug(new_path)
    cv2.imwrite(new_path, image_content)
    cut_height, cut_width, _ = image_content.shape
    logger.debug(f'{cut_height, cut_width}')
    end = time.time()
    logger.info(f"分割成功， 耗时: {end - start}s")
    info = {
        "path": new_path,
        "height": height,
        "width": width,
        "cut_height": cut_height
    }
    logger.debug(info)
    return info


def screenshot_util(driver, file_name=None, position: str = None):
    """
    截图并保存到预定路径
    @param driver
    @param file_name: foo.png or fool
    @param position: top_left\top_right\bottom_left\bottom_right
    @return:
    """
    logger.info("开始截图")
    if not file_name:
        raise ValueError("文件名不能为空")

    # 截图并保存到当前目录的image文件夹中
    relative_path = "screenshot"
    # 把文件名处理成test.png的样式
    if "." in file_name:
        file_name = file_name.split(r".")[0]
    if os.path.exists(relative_path) is False:
        os.mkdir(relative_path)
    time_str = time.strftime(f"%Y%m%d%H%M%S")
    file_name = f"{time_str}_{file_name}.jpg"

    file_path = os.path.join(relative_path, file_name)
    try:
        driver.screenshot(file_path)
    except:
        driver.screenshot(path=file_path)
    logger.info(f"保存至: {file_path}")
    # 对图片进行分割
    info = None
    if position is not None:
        info = cut_by_position(file_path, position)
        file_path = info.get("path")
    # 上传allure报告
    allure.attach.file(
        file_path,
        attachment_type=allure.attachment_type.PNG,
        name=f"{file_path}",
    )
    if position is not None:
        return info
    else:
        return file_path


def sanitize_filename(filename):
    """去除文件名中的非法字符"""
    # Windows 非法字符：\/:*?"<>|
    windows_illegal_chars = r'[\\/:\*\?"<>|]'
    # macOS 非法字符：/
    macos_illegal_chars = r'/'
    # Linux 非法字符：/
    linux_illegal_chars = r'/'

    # 根据当前操作系统选择对应的非法字符规则
    if platform.system() == 'Windows':
        illegal_chars = windows_illegal_chars
    elif platform.system() == 'Darwin':
        illegal_chars = macos_illegal_chars
    else:
        illegal_chars = linux_illegal_chars

    # 移除非法字符
    filename = re.sub(illegal_chars, '', filename)
    # 替换空格为下划线
    filename = filename.replace(' ', '_')
    # 去掉末尾的点号和空格
    filename = filename.rstrip('. ')
    return filename


def dict_to_str(source_dict: dict):
    """把字典转化成字符串，并调整成合规的文件名"""
    dict_str = '_'.join([sanitize_filename(f"{key}") for key, value in source_dict.items()])
    return dict_str


def calculate_time(func):
    """计算方法耗时"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"函数 {func.__name__} 的执行时间为: {execution_time} 秒")
        return result
    return wrapper


def retry(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        count = 0
        ret = None
        while count < 5:
            if count > 1:
                logger.info(f"操作失败，第{count}次重试.")
            try:
                ret = func(*args, **kwargs)
            except Exception as e:
                logger.debug(str(e))
                time.sleep(3)
                count += 1
                continue
            else:
                break
        else:
            logger.info("重试5次仍然失败.")
        return ret

    return wrapper


if __name__ == '__main__':
    print(get_free_port())



