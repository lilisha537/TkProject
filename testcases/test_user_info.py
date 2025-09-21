import requests


def test_get_user_info(user_session):
   """
   测试登录用户可以获取用户信息
   :return:
   """
   resp = user_session.request("GET", "/api/v1/auth/profile")
   print('获取用户信息',resp.json()["data"])
   assert resp.status_code == 200
   assert resp.json()["code"] == 200

#     :return:

def test_get_user_info_fail(session):
    """
    测试未登录用户不可以获取用户信息
    """
    resp = session.request("GET", "/api/v1/auth/profile")

    assert resp.status_code == 401