import sys


def general_api_case(module: str, host: str, case_name: str, method: str, url: str, assert_data: dict, headers: dict = None,
                     payload: dict = None):
    """生成api用例
    @param host:
    @param module: 所属模块
    @param case_name：用例名称
    @param method: 请求方法
    @param url: 请求url
    @param headers: 请求头
    @param payload: 请求数据
    @param assert_data: 断言数据
    {
        "path": "static.id",
        "method": "大于",
        "expect": 0
    }
    """
    api_name = url.split('/')[-1]  # 接口路径最后一段
    class_name = 'Test' + api_name.title()

    if method == 'get':
        payload_str = ', static=payload'
    elif method == 'post':
        payload_str = ', json=payload'
    else:
        payload_str = ''

    assert_method = assert_data.get('method', None)
    assert_path = assert_data.get('path', None)
    if assert_method == '等于':
        assert_str = f"self.assert_eq('{assert_path}')"
    elif assert_data == '大于':
        assert_str = f"self.assert_gt('{assert_path}')"
    else:
        sys.exit('暂不支持的断言方式')

    if headers:
        headers_str = f', headers={headers}'
    else:
        headers_str = ''

    api_case_template = f'''import qrunner
from qrunner import *


@module("{module}")
class {class_name}(qrunner.TestCase):

    @title('{case_name}')
    def test_{api_name}(self):
        payload = {payload}
        self.{method}({url}{payload_str}{headers_str})
        {assert_str}


if __name__ == '__main__':
    qrunner.main(
        host='{host}'
    )
'''

    return api_case_template


if __name__ == '__main__':
    print(general_api_case(
        module='查专利',
        host='https://patents-test.qizhidao.com',
        case_name='简单检索',
        method='get',
        url='/patentSearch/search',
        payload={"key": "华为"},
        headers={"token": "xxx"},
        assert_data={
            "path": "code",
            "method": "等于",
            "expect": 0
        }
    ))
