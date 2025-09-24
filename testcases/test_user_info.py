import allure
import pytest

from common.request_util import RequestUtil


# @allure.feature("User--Roles模块")
# class UserInfo:
#     base_url = "http://192.168.1.120:3011"
#     userType = ["personal","company"]
#
#     @allure.story("添加角色成功")
#     @pytest.mark.parametrize("username,password,nickname,email,userType,isActive",[
#         ("xiaozhang","xiaozhang123","测试人员","123123@qq.com","personal","True"),
#
#     ])
#     def test_user_info_add_success(self,token,username,password,nickname,email,
#                                    userType,isActive):
#         url = f"{self.base_url}/api/v1/users"
#         headers = {"Authorization": f"Bearer {token}"}
#         data = {"username":username,"password":password,"nickname":nickname,"email":email,
#                 "userType":userType,"isActive":isActive}
#
#         response = RequestUtil.send_request("POST",url,headers=headers,json=data)
#         assert response.status_code == 201
#
#         response_json = response.json()
#         assert response_json["code"] == 200
#
