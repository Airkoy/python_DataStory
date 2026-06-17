import requests


url = "http://api.dc.datastory.com.cn/weibo/2/app/getUrlByItemId"

data = {
    "ids": "4606349742180191",
    "token": "e7a4685c941137c475817a8110998fc0"
}

response = requests.post(url, data=data)

print(response.json())