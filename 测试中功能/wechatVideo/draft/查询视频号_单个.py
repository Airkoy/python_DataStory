import requests
import json
import openpyxl
import os
from datetime import datetime

headers = {
    "Content-Type": "application/json",
    "Authorization": os.environ["WECHAT_VIDEO_AUTHORIZATION"]
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
    result = search_uid("無茗葉")
    print(result)

if __name__ == "__main__":
    main()