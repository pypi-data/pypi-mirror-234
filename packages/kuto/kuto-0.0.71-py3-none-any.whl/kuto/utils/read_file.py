import json
import os
import inspect as sys_inspect

import yaml

from kuto.utils.excel import Excel, CSV
from kuto.utils.pytest_util import data


# 从json文件获取数据进行参数化
def file_data(file=None, key=None, row=None):
    # logger.debug(config.get_env())

    """
    @param row: 第几行，针对csv和excel文件
    @param file: 文件名
    @param key: 针对json和yaml文件
    """
    # 获取被装饰方法的目录
    stack_t = sys_inspect.stack()
    ins = sys_inspect.getframeinfo(stack_t[1][0])
    file_dir = os.path.dirname(os.path.abspath(ins.filename))
    # logger.debug(file_dir)
    parent_dir = os.path.dirname(file_dir)
    parent_dir_dir = os.path.dirname(parent_dir)
    parent_dir_dir_dir = os.path.dirname(parent_dir_dir)

    # 判断当前、父目录、爷目录、太爷爷目录下的test_data目录下是否有file_name文件
    path_list = [file_dir, parent_dir, parent_dir_dir, parent_dir_dir_dir]
    file_path = None
    full_list = []
    for _path in path_list:
        # environ = config.get_env()
        # if environ:
        #     full_path = os.path.join(_path, 'static', environ, static)
        # else:
        full_path = os.path.join(_path, 'static', file)
        full_list.append(full_path)
        # print(full_path)
        if os.path.isfile(full_path) is True:
            file_path = full_path
            break
    if file_path is None:
        raise Exception(f"can not found {file} in {full_list}")

    # logger.debug(file_path)
    if file_path.endswith(".json"):
        content = read_json(file_path, key)
    elif file_path.endswith(".yml"):
        content = read_yaml(file_path, key)
    elif file_path.endswith(".csv"):
        content = read_csv(file_path, row)
    elif file_path.endswith(".xlsx"):
        content = read_excel(file_path, row)
    else:
        raise TypeError("不支持的文件类型，仅支持json、yml、csv、xlsx")

    if content:
        return data(content)
    else:
        raise ValueError('数据不能为空')


def read_json(file_path, key=None):
    """
    读取json文件中的指定key
    @return
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    if isinstance(json_data, list):
        return json_data
    else:
        if key:
            return json_data[key]
        raise ValueError('key不能为空')


def read_yaml(file_path, key=None):
    """
    读取yaml文件中的指定key
    @param file_path:
    @param key:
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    if isinstance(yaml_data, list):
        return yaml_data
    else:
        if key:
            return yaml_data[key]
        raise ValueError('key不能为空')


def read_csv(file_path, row=None):
    """
    读取csv文件中的指定行
    @param file_path: 文件名
    @param row: 行数，从1开始
    """
    csv_file = CSV(file_path)
    if row:
        csv_data = [csv_file.read_row_index(row)]
    else:
        csv_data = csv_file.read_all()
    return csv_data


def read_excel(file_path, row=None):
    """
    读取excel文件中的指定行，暂时只支持读取第一个sheet
    @param file_path: 文件名
    @param row: 行数，从1开始
    """
    excel_file = Excel(file_path)
    if row:
        excel_data = [excel_file.read_row_index(row)]
    else:
        excel_data = excel_file.read_all()
    return excel_data


if __name__ == '__main__':
    print(read_json('static.json', key='names'))
    print(read_yaml('static.yml', key='names'))
    print(read_csv('static.csv', row=1))
    print(read_excel('static.xlsx', row=1))



