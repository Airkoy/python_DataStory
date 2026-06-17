import requests


url = "http://api.dc.datastory.com.cn/weibo/2/app/hotSearch/list"

data = {

    "token": "e7a4685c941137c475817a8110998fc0"
}

response = requests.get(url, params=data)

print(response.json())