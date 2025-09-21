#
# import pytest
# import allure
# from common.request_util import RequestUtil
#
# @allure.feature("登录模块")
# class TestLogin:
#     base_url = "http://120.78.123.12:3011"
#
#     @allure.story("用户登录成功")
#     @pytest.mark.parametrize("username,password",[("admin","20250805")])
#     def test_login_success(self,username,password):
#         url = f"{self.base_url}/api/v1/auth/login"
#         print(url)
#         payload = {"username":username,"password":password}
#
#         response = RequestUtil.send_request("POST",url,json=payload)
#         assert response.status_code == 201
#         response_json = response.json()
#         print(response_json)
#         assert "access_token" in response_json
#
#
#     @allure.story("用户登录失败-用户名或密码错误")
#     @pytest.mark.parametrize("username,password,expected_code", [
#         ("adminworing", "test123",401),
#         ("admin","testworing",401)
#     ])
#     def test_login_failure(self, username, password,expected_code):
#         url = f"{self.base_url}/api/v1/auth/login"
#         payload = {"username": username, "password": password}
#
#         response = RequestUtil.send_request("POST", url, json=payload)
#
#         assert response.status_code == expected_code
#
#
#
