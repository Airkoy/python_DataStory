import requests
import json
import openpyxl
import os
from datetime import datetime

headers = {
    "Content-Type": "application/json",
    "Authorization": os.environ["WECHAT_VIDEO_AUTHORIZATION"]
}

ADD_URL = "https://dc.datastory.com.cn/monitor/account/wechatVideo/add?uuu=banyan"


def add_monitor(name, uid):
    payload = json.dumps({"accounts": [{"name": name, "uid": uid}]}, ensure_ascii=False)
    try:
        resp = requests.post(ADD_URL, headers=headers, data=payload, timeout=30)
        return resp.text
    except Exception as e:
        return f"ERROR: {e}"

def main():
    result = add_monitor("無茗葉","v5_020b0a16610401000000000082d1175b4473ea000000b1afa7d8728e3dd43ef4317a780e33c2fcac55cd2d4812e1ad8c0fb536ef0a5871a8ce4c3e8da17e26f0629eb5ff28cadc9c4be5816685c8c47ef0e6c4673ac854c865b1c11ae1286034116261@stranger")
    print(result)

if __name__ == "__main__":
    main()