import requests
from datetime import datetime, time, timedelta
import json
import requests
from typing import Optional, Dict, Tuple


def get_token( url: str = 'https://dc.datastory.com.cn/auth/obtain') -> Optional[str]:
    """获取认证 token"""
    try:
        response = requests.post(url, data={"username": "hermes_admin@datastory.com.cn", "password": "hSm8W2MmuHy?J@!NzM2T"})
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


def get_account_token(account_name: str) -> Tuple[
    Optional[str], Optional[str], Optional[Dict]]:
    """根据账号名称从文件中读取凭据并获取 token 和 headers"""

    token = get_token()
    headers = create_headers(token) if token else None
    return account_name, token, headers


def get_today_timestamp(hour: int, minute: int) -> int:
    """
    获取当天指定时分对应的毫秒级时间戳（北京时间 UTC+8）
    """
    now_bj = datetime.now() + timedelta(
        hours=8) - datetime.now().utcoffset() if datetime.now().utcoffset() else datetime.now()
    # 更简洁的方式：直接用本地时间（服务器在中国即为北京时间）
    today = datetime.now()
    target = today.replace(hour=hour, minute=minute, second=0, microsecond=0)
    # 转为毫秒级时间戳
    return int(target.timestamp() * 1000)


def send_notify():
    # 动态设置当天的 17:30 和 22:30
    payload["startNotifyTime"] = get_today_timestamp(17, 30)
    payload["endNotifyTime"] = get_today_timestamp(22, 30)

    print(
        f"📅 startNotifyTime: {payload['startNotifyTime']} ({datetime.fromtimestamp(payload['startNotifyTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')})")
    print(
        f"📅 endNotifyTime:   {payload['endNotifyTime']} ({datetime.fromtimestamp(payload['endNotifyTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')})")
    print()

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            print("✅ 请求发送成功！")
            print("返回内容:", response.json())
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            print("返回内容:", response.text)

    except requests.exceptions.JSONDecodeError:
        print("✅ 请求发送成功，但返回内容不是JSON格式:")
        print(response.text)
    except Exception as e:
        print(f"🚨 发送请求时发生异常: {e}")


# 使用示例
if __name__ == "__main__":
    name, token, headers = get_account_token("admin账号")
    # if token:
    #     print(f"✅ 成功获取 '{name}' 的 token")
    #     print("Token:", token)
    #     print("headers=", json.dumps(headers, indent=2, ensure_ascii=False))
    # else:
    #     print("❌ 获取 token 失败")

    # 接口地址
    url = "https://dc.datastory.com.cn/admin/notify/save?uuu=banyan"

    # # 请求头
    # headers = {
    #     "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJoZXJtZXNfYWRtaW5AZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3ODA1NzQxODM3OSwicHciOiJVTlZQbWM3dCIsImV4cCI6MTc3ODY2MjIxOH0.SmOgGGeDi-HHXRwhVPzhcYggkbm00y309oannSNUiC3bP2Ip0_W_nGYku2i24HT3xq1lukVz6kNUXrInipJ5SQ",
    #     "Content-Type": "application/json",
    # }

    # 请求体
    payload = {
        "blockedAccounts": "抖音有限公司-用研部,抖音有限公司",
        "blockedType": 0,
        "content": "<p>数说聚合计划今天&nbsp;19：30 进行版本发布。<br/><br/>更新发布耗时：&nbsp;约&nbsp;30&nbsp;分钟，发布期间，如登录异常请稍后再刷新页面重试，望周知！</p>",
        "ignorePlatform": "embedded,oem",
        "isValid": 1,
        "msgType": "DEPLOY",
        "title": "聚合发布通知"
    }
    send_notify()
