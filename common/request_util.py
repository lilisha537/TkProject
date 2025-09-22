#请求封装,统一处理请求，日志和响应
import  requests
import json
import logging

class RequestUtil:
    session = requests.Session() #使用Session保持会话

    @staticmethod
    def send_request(method,url,**kwargs):
        """
        发送http请求并返回响应对象
        参数：method：请求方法（GET，POST，PUT，DELETE）
        url：请求的URL
        **kwargs：其他requests支持的参数，如params，data，json，headers
        """
        method =method.upper()
        try:
         #记录请求日志
            logging.info(f"Sending{method} request to {url}")
            logging.info(f"Request details:{kwargs.get('params','No params')},"
                     f"{kwargs.get('data','No data')},{kwargs.get('json','No JSON')}")

            response =RequestUtil.session.request(method,url,**kwargs)

            #记录响应日志
            logging.info(f"Response status code:{response.status_code}")
            logging.info(f"Response body:{response.text}")

            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed:{e}")
            raise
