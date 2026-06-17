import json
import requests
import datetime
from typing import Optional, Dict, Tuple


def get_token(username: str, password: str, url: str = 'https://dc.datastory.com.cn/auth/obtain') -> Optional[str]:
    """获取认证 token"""
    try:
        response = requests.post(url, data={"username": username, "password": password})
        response.raise_for_status()
        data = response.json()
        return data.get("data")  # 假设成功时 token 在 data 字段中
    except Exception as e:
        print(f"获取 token 失败: {e}")
        return None


def create_headers(token: str) -> Dict[str, str]:
    """构造请求头"""
    return {
        "Authorization": token,
        "Content-Type": "application/json"
    }


def get_account_token(account_name: str, filename: str = "accounts.json") -> Tuple[
    Optional[str], Optional[str], Optional[Dict]]:
    """根据账号名称从文件中读取凭据并获取 token 和 headers"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            accounts = json.load(f)
    except Exception as e:
        print(f"读取账号文件失败: {e}")
        return None, None, None

    if account_name not in accounts:
        print(f"账号 '{account_name}' 不存在于 {filename}")
        return None, None, None

    acc = accounts[account_name]
    token = get_token(acc["username"], acc["password"])
    headers = create_headers(token) if token else None
    return headers


def yyyymmddhhmmss_to_timestamp(time_str):
    """将 yyyymmddhhmmss 格式转换为时间戳"""
    dt = datetime.datetime.strptime(time_str, "%Y%m%d%H%M%S")
    return int(dt.timestamp()*1000)


# 使用示例
if __name__ == "__main__":
    # headers = get_account_token("koy账号")
    # print("headers=", json.dumps(headers, indent=2, ensure_ascii=False))

    url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

    headers = get_account_token("admin账号")
    time_list = ["20240417000000", "20260416235959"]
    timestamp = [yyyymmddhhmmss_to_timestamp(t) for t in time_list]
    # print(timestamp)
    # print(timestamp[0],timestamp[1])

    payload = json.dumps({
        "dataType": "GlobalMedia",
        "banyanType": "elf",
        "searchType": "Post",
        # "needReturnFields": "site_id,site_name,is_sensitive_politics,forum_name",
        "needReturnFields": "site_id,site_name,url",
        "searchCondition": [
            {"fieldName": "site_id", "operation": "eq", "fieldValue": ["1244369434"]},  # 1228001 reddit 1244369244 巴哈姆特 1244369434 tiktok
            {"fieldName": "ip_location", "operation": "nn", "fieldValue": [""]},
            {"fieldName": "poi_name", "operation": "nn", "fieldValue": [""]},
            {
                "fieldName": "publish_timestamp",
                "operation": "ltegte",
                # "fieldValue": [1713283200000, 1776355199000]  # 2024-04-17 00:00:00 ~ 2026-04-16 23:59:59
                "fieldValue": timestamp
            }
        ],
        "sortCondition": {
            "sortFieldName": "publish_timestamp",
            "order": "desc"
        },
        # "timeRange": "1777305600,1777391999",
        "timeRange": f"{timestamp[0]},{timestamp[1]}"
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    # print(f"{timestamp[0]},{timestamp[1]}")
    # print(payload)
