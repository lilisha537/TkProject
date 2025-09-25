import allure
import pytest
from pyexpat.errors import messages

from common.request_util import RequestUtil


@allure.feature("User--Roles模块")
class RolesInfo:
    base_url = "http://192.168.1.120:3011"

    @allure.story("添加角色成功")
    @pytest.mark.parametrize("username,password,nickname,email,user_type,company_name,is_active",[
        #personal 类型测试用例
        ("xiaozhang","xiaozhang123","测试人员","111@qq.com","personal","None","True"),
        ("xiaozz", "xiaozz123", "测试人员", "666@qq.com", "personal", "测试企业名称4", "True"),
        ("xiaowang", "xiaowang123", "测试人员", "222@qq.com", "personal", "None","False"),
        #company类型测试用例
        ("xiaoli", "xiaoli123", "企业人员", "333@qq.com", "company","测试企业名称1" "True"),
        ("xiaoha", "xiaoha123", "企业人员", "444@qq.com", "company", " ","True"),
        ("xiaokai", "xiaokai123", "企业人员", "555@qq.com", "company", "测试企业名称3" "False")

    ])
    def test_roles_info_add_success(self,token,username,password,nickname,email,user_type,company_name,is_active):
        url = f"{self.base_url}/api/v1/users"
        headers = {"Authorization": f"Bearer {token}"}

        data = {"username":username,"password":password,"nickname":nickname,"email":email,
                "userType":user_type,"isActive":is_active}

        if user_type == "company" and company_name is not None:
            data["companyName"]=company_name
        elif user_type == "personal" and company_name is not None:
            data["companyName"] = company_name

        response = RequestUtil.send_request("POST",url,headers=headers,json=data)

        assert response.status_code == 201
        response_json = response.json()

        assert response_json["userType"] == user_type
        assert response_json["isActive"] == is_active
        if user_type == "company":
            assert "companyName" in response_json
            assert response_json["companyName"] == company_name


@allure.story("添加角色失败")
@pytest.mark.parametrize("username,password,nickname,email,user_type,company_name,is_active", [
    # company类型未提供公司名称,状态激活或关闭
    ("xiao哈哈", "xiao哈哈i123", "企业人员", "777@qq.com", "company", " ","True"),
    ("xiao库", "xiao库123", "企业人员", "888@qq.com", "company", " ", "False"),
    #公司名为空或过长
    ("zhang哈哈", "zhang哈哈i123", "企业人员", "999@qq.com", "company", " ","True"),
    ("zh哈哈", "zh哈哈i123", "企业人员", "100@qq.com", "company", "A"*100,"True"),

])
def test_roles_info_add_success(self, token, username, password, nickname, email, user_type, company_name, is_active):
    url = f"{self.base_url}/api/v1/users"
    headers = {"Authorization": f"Bearer {token}"}

    data = {"username": username, "password": password, "nickname": nickname, "email": email,
            "userType": user_type, "isActive": is_active}

    if user_type == "company" and company_name is not None:
        data["companyName"] = company_name


    response = RequestUtil.send_request("POST", url, headers=headers, json=data)

    assert response.status_code == 400
    response_json = response.json()
    assert "message" in response_json


@allure.story("获取用户列表数据")
@pytest.mark.parametrize("page,page_size",[
    (1,10,200), #正常情况
    (0,10,400),#边界情况，页码从1开始
    (1,0,400),#页大小过小，正常情况页大小至少为1
    (None,10,200), #可能使用默认页码，缺失页码使用默认值
    ("abc",10,400,) #无效页码--错误数据类型
])
def test_roles_info_list_success(self,token,page,page_size):
    url = f"{self.base_url}/api/v1/users"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"page":page,"page_size":page_size}
    if page is not None:
        data["page"] =page
    if page_size is not None:
        data["size"] =page_size


    response = RequestUtil.send_request("GET",url,headers=headers)
    assert response.status_code == 200

    response_json = response.json()
    assert "total_count" in data
    assert isinstance(response_json["data"]["records"],list)
    assert  'id' in response_json["data"]["records"][0]

@allure.story("获取用户列表失败")
def test_roles_info_list_fail(self,token,page,page_size):
    url = f"{self.base_url}/api/v1/users"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"page":page,"page_size":page_size}
    if page is not None:
        data["page"] =page
    if page_size is not None:
        data["size"] =page_size

    response = RequestUtil.send_request("GET",url,headers=headers)
    assert response.status_code == 400
