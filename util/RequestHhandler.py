import json
import requests
# 导入解析功能：
from bs4 import BeautifulSoup
# 引入日志功能：
from util.LogHandler import logger
class RequestHandler(object):
    # 发请求功能：
    def get_response(self, item):
        # 获得请求结果：
        # logger().info(item)
        return self._send_msg(item)
    def _send_msg(self, item):
        # 发请求的操作(私有的)：
        response = requests.request(
            # 请求类型：
            method=item['case_method'],
            # 请求url：
            url=item['case_url'],
            # 处理请求中携带的data数据(私有的)
            data=self._check_data_msg(item),
            # 处理请求中的请求头(私有的)
            headers=self._check_headers_msg(item)
        )
        # 分不同的json返回类型处理：
        Content_Type = response.headers['Content-Type'].split('/')[0]
        # 反射：
        if hasattr(self, '_check_{}_response'.format(Content_Type)):
            obj = getattr(self, '_check_{}_response'.format(Content_Type))
            res = obj(response, item)
        else:
            pass
        return res
    def _check_application_response(self, response, item):
        # 处理json类型的响应：
        response = response.json()
        expect = json.loads(item['case_expect'])
        for key, value in expect.items():
            # 意味着预期值的字段跟实际请求结果的字段不一致：断言失败
            if value != response.get(key, None):
                logger().info('请求：{} 断言失败，预期值是：[{}] 实际执行结果：[{}], 相关参数:{}'.format(
                    item['case_url'],
                    value,
                    response.get(key, None),
                    item
                ))
                return (value, response.get(key, None))
        else:
            # 断言成功
            return (value, response.get(key, None))
    def _check_text_response(self, response, item):
        # 处理文本类型的响应：
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        return (title, item['case_expect'])
    def _check_image_response(self, response, item):
        # 处理jpeg图片类型的响应：
        pass
    def _check_data_msg(self, item):
        # 处理请求中携带的data数据(私有的)：
        if item.get('case_data', None):
            # 如果请求中有data参数：
            pass
        else:
            return {}
    def _check_headers_msg(self, item):
        # 处理请求中的请求头(私有的)、预留接口负责处理，请求头相关的逻辑
        # 自定义一些固定的请求头，也可以将Excel表格中的特殊请求头更新到这个字典中
        headers = {}
        if item.get('case_headers', None):
            headers.update(json.loads(item['case_headers']))
        return headers
if __name__ == '__main__':
    pass