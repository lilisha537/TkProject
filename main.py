# import json
#
# import requests
#
# session = requests.Session()
# base_url = "https://www.darenxingtan.com/"
#
# def chek_1():
#     with open("schema.json",encoding="utf-8") as f:
#         schema = json.loads(f.read())
#
#         for path in schema['paths']:
#             for method in schema['paths'][path]:
#                 url = base_url+path
#                 resp = session.request(method, url)
#                 print(resp.status_code,resp.text,method,url)