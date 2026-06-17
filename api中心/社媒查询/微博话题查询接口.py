import requests


url = "http://api.dc.datastory.com.cn/weibo/2/app/topic/search"

data = {
    "keyword": "python",
    "token": "e7a4685c941137c475817a8110998fc0",
    "page": "0",
}

response = requests.post(url, data=data)

print(response.json())


