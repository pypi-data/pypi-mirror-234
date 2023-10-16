import kuto


class TestApiDemo(kuto.Case):
    """接口demo"""

    @kuto.title("一般请求")
    def test_normal_req(self):
        payload = {"type": 2}
        headers = {
            "user-agent-web": "X/b67aaff2200d4fc2a2e5a079abe78cc6"
        }
        self.post('/qzd-bff-app/qzd/v1/home/getToolCardListForPc',
                  json=payload, headers=headers)
        self.assert_eq('code', 0)

    @kuto.title("文件上传")
    def test_upload_file(self):
        path = '/qzd-bff-patent/patent/batch/statistics/upload'
        files = {'static': open('../static/号码上传模板_1.xlsx', 'rb')}
        self.post(path, files=files)
        self.assert_eq('code', 0)

    @kuto.title("form请求")
    def test_form_req(self):
        url = '/qzd-bff-patent/image-search/images'
        file_data = (
            'logo.png',
            open('../static/logo.png', 'rb'),
            'image/png'
        )
        fields = {
            'key1': 'value1',  # 参数
            'imageFile': file_data  # 文件
        }
        form_data = kuto.MultipartEncoder(fields=fields)
        headers = {'Content-Type': form_data.content_type}
        self.post(url, data=form_data, headers=headers)
        self.assert_eq("code", 0)


if __name__ == '__main__':
    kuto.main(host='https://app-test.qizhidao.com')
