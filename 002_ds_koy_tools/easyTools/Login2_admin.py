import json
import requests

url = 'https://dc.datastory.com.cn/auth/obtain'
# url = 'http://dc.dev.datastory.com.cn/auth/obtain'


# 管理员账号
data = {
    "username": "hermes_admin@datastory.com.cn",
    "password": "hSm8W2MmuHy?J@!NzM2T"
    # "password": "123456", # 测试环境
}

#
# # 其他账号
# data = {
#     "username": "aldvq967@163.com",
#     "password": "aldvq967"
# }

response = requests.post(url, data=data)

# 直接提取token并构建headers
token = response.json()['data']
headers = {
    "Content-Type": 'application/json',
    'Authorization': token,
}
# 打印响应结果
# print('Response:', response.text)

print('headers =', json.dumps(headers, indent=4))
print(token)
