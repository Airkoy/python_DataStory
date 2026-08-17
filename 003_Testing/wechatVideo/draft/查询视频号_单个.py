import requests
import json
import openpyxl
import os
from datetime import datetime

url = 'https://dc.datastory.com.cn/auth/obtain'

data = {
    "username": "hermes_admin@datastory.com.cn",
    "password": "hSm8W2MmuHy?J@!NzM2T"
    # "password": "123456", # 测试环境
}

response = requests.post(url, data=data)

# 直接提取token并构建headers
token = response.json()['data']
headers = {
    "Content-Type": 'application/json',
    'Authorization': token,
}

SEARCH_URL = "https://dc.datastory.com.cn/monitor/account/wechatVideo/batchSearch?uuu=banyan"


def search_uid(name):
    data = {"name": [name]}
    try:
        resp = requests.post(SEARCH_URL, headers=headers, data=json.dumps(data), timeout=10)
        result = resp.json()
        uids = result.get("data", {}).get("uids", [])
        if uids:
            return uids[0].get("uid", "")
        return ""
    except Exception as e:
        print(f"[ERROR] {name}: {e}", flush=True)
        return ""

def main():
    result = search_uid("QQ浏览器")
    print(result)

if __name__ == "__main__":
    main()