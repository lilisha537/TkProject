#
# import allure
# import pytest
# import requests
#
# from common.request_util import RequestUtil
#
#
# @allure.feature("注册模块")
# class TestRegister():
#     base_url = "http://120.78.123.12:3011"
#
#     @allure.story("注册成功")
#     @pytest.mark.parametrize("username,email,password,userType",[("admin2","1234509@qq.com","20250805097","个人用户")])
#     def test_register_success(self,username,email,password,userType):
#         url = f"{self.base_url}/api/v1/auth/register"
#
#         payload = {"username":username,"password":password,"email":email,"userType":userType}
#
#         response = RequestUtil.send_request("POST",url,json=payload)
#
#
#         response_json = response.json()
#         print(response_json)
#
#     @allure.story("注册失败--请求参数错误或用户已存在")
#     @pytest.mark.parametrize("username,email,password,userType",[("admin1","123456@qq.com","20250805","个人用户")])
#     def test_register_fail(self,username,email,password,userType):
#         url = f"{self.base_url}/api/v1/auth/register"
#
#         payload = {"username":username,"password":password,"email":email,"userType":userType}
#
#         response = RequestUtil.send_request("POST",url,json=payload)
#
#         assert response.status_code == 400
