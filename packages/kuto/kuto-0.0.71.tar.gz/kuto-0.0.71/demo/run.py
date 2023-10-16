import kuto


if __name__ == '__main__':
    # 执行多个用例文件，主程序入口

    # 执行接口用例
    kuto.main(
        platform="api",
        host='https://app-pre.qizhidao.com',
        path='tests/test_api.py'
    )


