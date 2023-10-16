# @Time    : 2022/2/22 9:35
# @Author  : kang.yang@qizhidao.com
# @File    : request.py
import json as json_util
import logging
import re
from functools import wraps

import jmespath
from jsonschema import validate, ValidationError
from requests.packages import urllib3
from urllib import parse

import requests

from kuto.utils.config import config
from kuto.utils.log import logger

# 去掉requests本身的日志
urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(logging.CRITICAL)

# 去掉不设置证书的报警
urllib3.disable_warnings()


def formatting(msg):
    """formatted message"""
    if isinstance(msg, dict):
        return json_util.dumps(msg, indent=2, ensure_ascii=False)
    return msg


def request(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("-------------- Request -----------------[🚀]")
        # 给接口带上默认域名
        # 从配置文件中读取域名
        host = config.get_common("base_url")
        # 如果接口路径不以http开头，把域名写到key为url的位置参数中或者第一个参数中
        if "url" in kwargs:
            path: str = kwargs.get("url", "")
            if not path.startswith('http'):
                url = parse.urljoin(host, path)
                kwargs["url"] = url
            else:
                url = path
        else:
            path = list(args)[1]
            if not path.startswith('http'):
                url = parse.urljoin(host, path)
                args_list = list(args)
                args_list[1] = url
                args = tuple(args_list)
            else:
                url = path

        # 请求头处理，写入登录态
        default_headers = config.get_common("headers")
        if default_headers:
            kwargs["headers"] = default_headers
        header_user_set = kwargs.pop("headers", {})
        if header_user_set:
            kwargs["headers"] = header_user_set

        # 更新超时时间
        timeout_user_set = kwargs.pop("timeout", None)  # 用例脚本中设置的超时时间
        kwargs["timeout"] = timeout_user_set if timeout_user_set else 10

        # 发送请求
        r = func(*args, **kwargs)

        # 输出请求参数日志
        logger.debug("[method]: {m}      [url]: {u}".format(m=func.__name__.upper(), u=url))
        auth = kwargs.get("auth", "")
        if auth:
            logger.debug(f"[auth]:\n {formatting(auth)}")
        logger.debug(f"[headers]:\n {formatting(dict(r.request.headers))}")
        cookies = kwargs.get("cookies", "")
        if cookies:
            logger.debug(f"[cookies]:\n {formatting(cookies)}")
        params = kwargs.get("params", "")
        if params:
            logger.debug(f"[params]:\n {formatting(params)}")
        data = kwargs.get("static", "")
        if data:
            logger.debug(f"[static]:\n {formatting(data)}")
        json = kwargs.get("json", "")
        if json:
            logger.debug(f"[json]:\n {formatting(json)}")

        # 保存响应结果并输出日志
        status_code = r.status_code
        headers = r.headers
        content_type = headers.get("Content-Type")
        ResponseResult.status_code = status_code
        logger.info("-------------- Response ----------------")
        logger.debug(f"[status]: {status_code}")
        logger.debug(f"[headers]: {formatting(headers)}")
        try:
            resp = r.json()
            logger.debug(f"[type]: json")
            logger.debug(f"[response]:\n {formatting(resp)}")
            ResponseResult.response = resp
        except Exception:
            # 非json响应数据，根据响应内容类型进行判断
            logger.info("response is not json type static.")
            if content_type is not None:
                if "text" not in content_type:
                    logger.debug(f"[type]: {content_type}")
                    logger.debug(f"[response]:\n {r.content}")
                    ResponseResult.response = r.content
                else:
                    logger.debug(f"[type]: {content_type}")
                    logger.debug(f"[response]:\n {r.text}")
                    ResponseResult.response = r.text
            else:
                logger.debug('ContentType为空，响应异常！！！')
                ResponseResult.response = r.text

    return wrapper


class ResponseResult:
    # 并发执行不会串数据，是因为我用的是多进程而不是多线程吧???
    status_code = 200
    response = None


class HttpReq(object):
    @request
    def get(self, url, params=None, verify=False, **kwargs):
        return requests.get(url, params=params, verify=verify, **kwargs)

    @request
    def post(self, url, data=None, json=None, verify=False, **kwargs):
        return requests.post(url, data=data, json=json, verify=verify, **kwargs)

    @request
    def put(self, url, data=None, json=None, verify=False, **kwargs):
        if json is not None:
            data = json_util.dumps(json)
        return requests.put(url, data=data, verify=verify, **kwargs)

    @request
    def delete(self, url, verify=False, **kwargs):
        return requests.delete(url, verify=verify, **kwargs)

    @property
    def response(self):
        """
        Returns the result of the response
        :return: response
        """
        return ResponseResult.response

    # 断言
    @staticmethod
    def assert_status(status_code):
        """
        状态码
        """
        actual_code = ResponseResult.status_code
        logger.info(f"断言: {actual_code} 等于 {status_code}")
        assert (
                actual_code == status_code
        ), f"{ResponseResult} != {status_code}"

    @staticmethod
    def assert_schema(schema, response=None) -> None:
        """
        Assert JSON Schema
        doc: https://json-schema.org/
        """
        logger.info(f"assertSchema -> {formatting(schema)}.")

        if response is None:
            response = ResponseResult.response

        try:
            validate(instance=response, schema=schema)
        except ValidationError as msg:
            assert "Response static" == "Schema static", msg

    @staticmethod
    def assert_eq(path, value):
        """
        等于
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 等于 {value}")
        assert search_value == value, f"{search_value} != {value}"

    @staticmethod
    def assert_neq(path, value):
        """
        不等于
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不等于 {value}")
        assert search_value != value, f"{search_value} == {value}"

    @staticmethod
    def assert_leq(path, value):
        """
        长度等于
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 等于 {value}")
        assert len(search_value) == value, f"{len(search_value)} != {value}"

    @staticmethod
    def assert_lgt(path, value):
        """
        长度大于等于
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 大于等于 {value}")
        assert len(search_value) >= value, f"{len(search_value)} < {value}"

    @staticmethod
    def assert_llt(path, value):
        """
        长度小于等于
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 小于等于 {value}")
        assert len(search_value) <= value, f"{len(search_value)} > {value}"

    @staticmethod
    def assert_gt(path, value):
        """
        大于等于
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 大于等于 {value}")
        assert search_value >= value, f"{search_value} < {value}"

    @staticmethod
    def assert_lt(path, value):
        """
        小于等于
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 小于等于 {value}")
        assert search_value <= value, f"{search_value} 大于 {value}"

    @staticmethod
    def assert_rg(path, start, end):
        """
        范围
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 在 [{start}, {end}] 范围内")
        assert (search_value >= start) & (
                search_value <= end
        ), f"{search_value} 不在[{start}, {end}]范围内"

    @staticmethod
    def assert_in(path, value):
        """
        被包含
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 被 {value} 包含")
        assert search_value in value, f"{value} 不包含 {search_value}"

    @staticmethod
    def assert_nin(path, value):
        """
        不被包含
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不被 {value} 包含")
        assert search_value not in value, f"{value} 包含 {search_value}"

    @staticmethod
    def assert_ct(path, value):
        """
        包含
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 包含 {value}")
        assert value in search_value, f"{search_value} 不包含 {value}"

    @staticmethod
    def assert_nct(path, value):
        """
        不包含
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不包含 {value}")
        assert value not in search_value, f"{search_value} 包含 {value}"

    @staticmethod
    def assert_type(path, value_type):
        """
        字段类型
        """
        if not isinstance(value_type, type):
            if value_type == "int":
                value_type = int
            elif value_type == "str":
                value_type = str
            elif value_type == "list":
                value_type = list
            elif value_type == "dict":
                value_type = dict
            else:
                value_type = str

        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 是 {value_type} 类型")
        assert isinstance(
            search_value, value_type
        ), f"{search_value} 不是 {value_type} 类型"

    @staticmethod
    def assert_start(path, value):
        """
        以什么开始
        """
        search_value: str = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 以 {value} 开头")
        assert search_value.startswith(value), f"{search_value} 不以 {value} 开头"

    @staticmethod
    def assert_end(path, value):
        """
        以什么结束
        """
        search_value: str = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 以 {value} 结尾")
        assert search_value.endswith(value), f"{search_value} 不以 {value} 结尾"

    @staticmethod
    def assert_match(path, value):
        """正则匹配"""
        search_value = jmespath.search(path, ResponseResult.response)
        match_obj = re.match(r"" + value, search_value, flags=re.I)
        logger.info(f"断言: {search_value} 匹配正则表达式 {value} 成功")
        assert match_obj is not None, f"结果 {search_value} 匹配失败"


