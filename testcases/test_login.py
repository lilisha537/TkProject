
import pytest
import allure
from pygments.styles.dracula import yellow
from requests import session

from common.request_util import RequestUtil

@allure.feature("登录模块")
class TestLogin:
    base_url = "http://192.168.1.120:3011"

    @allure.story("用户登录成功")
    @pytest.mark.parametrize("username,password",[
        ("admin","20250805")
    ])

    @pytest.fixture(scope="session")
    def test_login_success(self,username,password):
        url = f"{self.base_url}/api/v1/auth/login"
        print(url)
        data = {"username":username,"password":password}

        response = RequestUtil.send_request("POST",url,json=data)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["code"]==200
        assert "access_token" in response_json["data"]
        #从响应中提取token
        token = response_json["data"]["access_token"]
        #将token返回给使用该fixture的测试函数
        yield token


    @allure.story("用户登录失败-用户名或密码错误")
    @pytest.mark.parametrize("username,password,expected_code", [
        #用户名错误
        ("adminworing", "test123",401),
        #密码错误
        ("admin","testworing",401)
    ])
    def test_login_failure(self, username, password,expected_code):
        url = f"{self.base_url}/api/v1/auth/login"
        data = {"username": username, "password": password}

        response = RequestUtil.send_request("POST", url, json=data)

        assert response.status_code == expected_code


    @allure.story("获取用户信息成功")
    # @pytest.mark.parametrize("username,password", [
    #     ("admin","20250805")
    # ])
    def test_profile_success(self,auth_token):
        """获取用户信息接口，需要token认证"""
        url = f"{self.base_url}/api/v1/auth/profile"
        headers = {"Authorization":f"Bearer {auth_token}"}

        response = RequestUtil.send_request("GET", url, headers=headers)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["code"] == 200
        assert "username" in response_json["data"]





