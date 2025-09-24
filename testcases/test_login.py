from http.client import responses

import pytest
import allure

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
    def test_user_info_success(self,token):
        """获取用户信息接口，需要token认证"""
        url = f"{self.base_url}/api/v1/auth/profile"
        headers = {"Authorization":f"Bearer {token}"}

        response = RequestUtil.send_request("GET", url, headers=headers)
        response_json = response.json()

        assert response.status_code == 200
        assert response_json["code"] == 200
        assert "username" in response_json["data"]


    @allure.story("获取用户信息失败--token格式不正确")
    @pytest.mark.parametrize("token,expected_code",[
        (" ",401),  #token为空
        ("InvalidTokenFormat",401), #token 格式不正确
        ("expired_token",400), #token失效    #token对应的用户不存在
    ],indirect=["token"]   #通过indirect参数指定哪些参数名作为fixture来解析
                             )
    def test_user_info_token_fail(self,token,expected_code):
        """获取token格式不正确，获取不到用户信息"""
        url = f"{self.base_url}/api/v1/auth/profile"
        headers = {"Authorization" : f"Bearer{token}"}

        response = RequestUtil.send_request("GET",url,headers=headers)

        assert response.status_code == expected_code



    @allure.story("获取用户信息失败--用户ID格式不正确")
    @pytest.mark.parametrize("user_id","expected_code",[
        (" ",400),
        ("invalid_string",400),
        ("99999",400)
    ])
    def test_user_info_userid_fail(self,token,user_id,expected_code):
        """测试用户ID不正确，无法获取信息"""
        url = f"{self.base_url}/api/v1/auth/profile"
        headers = {"Authorization": f"Bearer {token}"}

        response = RequestUtil.send_request("GET",url,headers=headers)

        assert response.status_code == 400  # 400参数错误

    @allure.story("使用A的token获取B用户信息失败")
    def test_user_info_insufficient_permissions_fail(self):
        """A的权限不能访问B的信息"""
        user_a_token = "enJyddckddisdcddkasession"
        url = f"{self.base_url}/api/v1/auth/profile"
        params = {"user_id":123} #用户B的id
        headers = {"Authorization":f"Bearer{user_a_token}"}

        response = RequestUtil.send_request("GET",url,headers=headers,params=params)
        assert response.status_code == 401 #未授权

        response_data = response.json()
        assert "permission" in response_data.get("message"," ").lower()

    @allure.story("使用mocking模拟服务器返回500")
    def test_user_info_server_error(self,mocker,token):
        """使用mocking模拟服务器返回5xx错误"""

        from unittest.mock import Mock
        #创建一个模拟的response对象，状态码为500
        mock_response= Mock()
        mock_response.status_code = 500
        mock_response.json.return_value={"error":"Internal Server Error"}

        #使用mocker 替换request.get 使其返回模拟的response
        mocker.patch('requests.get',return_value=mock_response)

        url = f"{self.base_url}/api/v1/auth/profile"
        headers = {"Authorization": f"Bearer {token}"}
        response = RequestUtil.send_request("GET",url,header=headers) #此时返回模拟的500响应

        assert response.status_codes == 500
        assert  "Internal Server Error" in response.json().get("error"," ")


    @allure.story("成功获取不同权限角色token，查看对应菜单")
    def test_user_info_menus_success(self,token):
        """登录后获取到对应用户的登录token，进行请求获取菜单"""

        headers = {"Authorization": f"Bearer {token}"}
        url = f"{self.base_url}/api/v1/auth/menus"

        response = RequestUtil.send_request("GET",url,headers=headers)

        assert response.status_code == 200

        menu_data = response.json()  #解析响应json
        menu_list = menu_data['data']
        assert isinstance(menu_list,list),"响应数据应为列表形式"
        assert len(menu_list) > 0, "用户菜单不为空"
        #检查是否存在某个已知菜单项
        assert any(item['name'] == '菜单管理' for item in menu_list)


    @allure.story("获取不到角色token，不能查看对应菜单")
    @pytest.mark.parametrize("token,expected_code", [
        (" ", 401),  # token为空
        ("InvalidTokenFormat", 401)
    ])
    def test_user_info_menus_fail(self, token,expected_code):
        """获取不到对应用户的登录token，无法获取菜单 """

        headers = {"Authorization": f"Bearer {token}"}
        url = f"{self.base_url}/api/v1/auth/menus"

        response = RequestUtil.send_request("GET", url, headers=headers)

        assert response.status_code == expected_code