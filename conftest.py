# # pytest--夹具配置
# import pytest
#
# from libs import APISession, ApiInfo
#
# # _base_url = "https://www.darenxingtan.com/"
# _base_url = "http://192.168.1.101:3011"
# _user_info = {"username": "admin", "password": "20250805"}  # 测试账号
#
#
# class ApiList:
#     # 获取验证码 = ApiInfo(
#     #     method="POST",
#     #     url="/api/v1/auth/login",
#     #     body = {"username":" ","password":" "}
#     # )
#     login = ApiInfo(
#         method="POST",
#         url="/api/v1/auth/login",
#         body=_user_info,
#         code=201,
#     )
#
#     register = ApiInfo(
#         method="POST",
#         url ="/api/v1/auth/register",
#         username = "username",
#         email ="test@example.com",
#         password ="123456",
#         userType = "personal",
#         companyName = "示例公司"
#     )
#
#
# _api_info = ApiList()  # 变量
#
#
# @pytest.fixture(scope="session")
# def api_info():
#     return _api_info
#
#
# @pytest.fixture()
# def session():
#     """
#     未登录状态的seesion
#     :return:
#     """
#     return APISession(base_url=_base_url)
#
#
# @pytest.fixture(scope="session")
# def user_session(api_info):
#     print('拿到api_info', api_info)
#     """
#     已登录状态的session
#     :return:111111111111112323
#     """
#     session = APISession(base_url=_base_url)
#     # 1、登录获取token
#     # 1.1获取验证码
#     # data=api.body  #设置传递的参数
#     # data['username'] = _user_info['username']
#     # resp = session.request(api.method,api.url,json = data)
#     # #判断返回的值和响应格式及响应里的code是否正确
#     # assert resp.status_code == api.code
#     # assert resp.json().keys() ==api.resp_body.keys()
#     # assert resp.json()["code"] == 200
#     #
#     # #断言通过就会有msgCode短信验证码
#     # msgCode = resp.json()['data'] #短信验证码
#
#     # 1.2获取验证码
#     api = api_info.login
#     print(api)
#     #     data = api.body  # 设置传递的参数
#     #     data["username"] = _user_info["username"]
#     #     data ["password"] =_user_info["password"]
#     data = api.body
#     resp = session.request(api.method, api.url, json=data)
#     # 判断返回的值和响应格式及响应里的code是否正确
#     assert resp.status_code == api.code
#     assert resp.json()["code"] == 200
#
#     #断言成功得到token
#     res = resp.json()["data"]  # token
#     #2、把token添加到session请求头
#     session.headers["Authorization"]= "Bearer "+ res['access_token']
#     # print(session.headers)
#     return session


# #更高级的获取token方法---缓存文件
# import  pytest
# import os
# import pickle   #使用json内存缓存如cachetools
#
# from common.request_util import RequestUtil
#
#
# def _login_and_get_token():
#     """实际登录逻辑"""
#     url = "http://192.168.1.120:3011/api/v1/auth/login"
#     data = {"username":"admin","password":"test123"}
#     response = RequestUtil.send_request("POST",url,json=data)
#     return response.json()["data"]["token"]
#
# @pytest.fixture(scope="session")
# def auth_token_with_cache():
#     """
#     带缓存的token fixture ，优先从缓存文件中读取token，如果没有或失效则需要重新登录
#     :return:
#     """
#     cache_file = "token_cache.pkl"
#
#      #尝试从缓存读取
#     if os.path.exists(cache_file):
#         try:
#             with open(cache_file,'rb')as f:
#                 cached_token = pickle.load(f)
#                 print("从缓存中读取到token")
#                 return cached_token
#         except Exception as e:
#             print(f"读取缓存失败：{e},重新登录获取")
#
#     #缓存不存在或无效，则从新登录
#     new_token = _login_and_get_token()
#     print("重新获取token")
#
#     #写入缓存
#     try:
#         with open(cache_file,'wb')as f:
#             pickle.dump(new_token,f)
#     except Exception as e:
#         print(f"写入缓存失败：{e}")
#
#     return new_token
#
# #可选清理的fixture
# @pytest.fixture(scope="session",autouse=True)
# def cleanup_token_cache(auth_token_with_cache):
#     """测试回话结束后清理缓存文件"""
#     yield
#     cache_file = "token_cache.pkl"
#     if os.path.exists(cache_file):
#         os.remove(cache_file)
#         print("测试会话结束，已清理token缓存文件")

import pytest


@pytest.fixture(scope="session")
def expired_token():
    #存放无效或过期token,实际需要替换使用真实的token
    expired_token_string ="eyJhbGciOiJIUzIiNiyibucunzaideyonghu.fake_expired_token_signature"

    return expired_token_string

#高级玩法:
#import pytest
# import jwt
# import time
# import datetime
#
# @pytest.fixture(scope="session")
# def expired_token():
#     """
#     生成一个立即可用的过期 JWT Token。
#     通过设置 'exp' (Expiration Time) 声明为一个过去的时间戳来实现。
#     """
#     # 你的密钥，应与服务端验证 Token 时使用的密钥一致
#     secret_key = 'your-secret-key-for-testing'
#     # payload 数据，可根据你的实际 Token 结构调整
#     payload = {
#         'user_id': 123,
#         'username': 'test_user',
#         # 将过期时间设置为当前时间之前（例如 10 秒前），确保 Token 生成后立即过期
#         'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=10)
#     }
#     # 使用 HS256 算法生成 Token
#     expired_token = jwt.encode(payload, secret_key, algorithm='HS256')
#
#     # jwt.encode 可能返回 bytes 或字符串，确保返回字符串
#     if isinstance(expired_token, bytes):
#         expired_token = expired_token.decode('utf-8')
#
#     return expired_token









