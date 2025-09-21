# pytest--夹具配置
import pytest

from libs import APISession, ApiInfo

# _base_url = "https://www.darenxingtan.com/"
_base_url = "http://192.168.1.101:3011"
_user_info = {"username": "admin", "password": "20250805"}  # 测试账号


class ApiList:
    # 获取验证码 = ApiInfo(
    #     method="POST",
    #     url="/api/v1/auth/login",
    #     body = {"username":" ","password":" "}
    # )
    login = ApiInfo(
        method="POST",
        url="/api/v1/auth/login",
        body=_user_info,
        code=201,
    )


_api_info = ApiList()  # 变量


@pytest.fixture(scope="session")
def api_info():
    return _api_info


@pytest.fixture()
def session():
    """
    未登录状态的seesion
    :return:
    """
    return APISession(base_url=_base_url)


@pytest.fixture(scope="session")
def user_session(api_info):
    print('拿到api_info', api_info)
    """
    已登录状态的session
    :return:111111111111112323
    """
    session = APISession(base_url=_base_url)
    # 1、登录获取token
    # 1.1获取验证码
    # data=api.body  #设置传递的参数
    # data['username'] = _user_info['username']
    # resp = session.request(api.method,api.url,json = data)
    # #判断返回的值和响应格式及响应里的code是否正确
    # assert resp.status_code == api.code
    # assert resp.json().keys() ==api.resp_body.keys()
    # assert resp.json()["code"] == 200
    #
    # #断言通过就会有msgCode短信验证码
    # msgCode = resp.json()['data'] #短信验证码

    # 1.2获取验证码
    api = api_info.login
    print(api)
    #     data = api.body  # 设置传递的参数
    #     data["username"] = _user_info["username"]
    #     data ["password"] =_user_info["password"]
    data = api.body
    resp = session.request(api.method, api.url, json=data)
    # 判断返回的值和响应格式及响应里的code是否正确
    assert resp.status_code == api.code
    assert resp.json()["code"] == 200

    #断言成功得到token
    res = resp.json()["data"]  # token
    #2、把token添加到session请求头
    session.headers["Authorization"]= "Bearer "+ res['access_token']
    # print(session.headers)
    return session
