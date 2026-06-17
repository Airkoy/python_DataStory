import requests
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://dc.datastory.com.cn/application/market/job/v1/run"
DEFAULT_TIMEOUT = 30  # 秒


def load_token() -> str:
    """从环境变量或配置文件读取 Authorization token"""
    token = os.environ.get("DS_AUTH_TOKEN")
    if token:
        return token
    # 回退到硬编码（生产环境应移除）
    logger.warning("未检测到环境变量 DS_AUTH_TOKEN，使用内置 token（不推荐）")
    return "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3ODE0NDQyNzU0NCwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3Nzg3NDkyMjd9.F_D9ftMi3qM38MwtBNXtqnHo61sQ0azLNJ4QS5G16hDlReMW3wscJqNoAqHxXHt5xqiQ8q6T3qxSYlB437umsQ"


def build_payload() -> dict:
    """构建请求体"""
    return {
        "appId": 12,
        "exportConfig": {"local": {}},
        "globalConfig": {
            "email": "koy@datastory.com.cn",
            "emailMode": 2,
            "isKeepTrend": False,
            "isRealTime": {"COMMENT": 1, "INTERACTION": 1, "POST": 0},
        },
        "jobName": "快手-bugtest-api创建-re2",
        "scheduleConfig": {
            "commentDelayList": [0, 4],
            "commentDelayUnit": "d",
            "endDataTime": 1780847999000,
            "interactionDelayList": [1, 4],
            "interactionDelayUnit": "d",
            "interval": 1,
            "postDelay": 0,
            "schedStartTime": 1778169600000,
            "searchStartTime": 2,
            "searchUnit": "d",
            "startDataTime": 1749398399999,
            "type": "SIMPLE",
            "unit": "d",
            "useInteractionDefaultDelay": False,
        },
        "scopeId": 6,
        "sheetId": 66560,
        "sourceConfig": {
            "condition": [
                {
                    "filterwords": "",
                    "keywords": " 电动",
                    "name": "分析对象1",
                    "uid": "646544542",
                }
            ],
            "fieldMode": 0,
            "input": "uid",
            "isCoproduce": 0,
            "matchType": ["content"],
            "output": ["POST-video#0", "POST-image#0", "INTERACTION", "COMMENT"],
        },
    }


def run_job() -> dict:
    """发送 POST 请求并返回响应 JSON"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": load_token(),
    }
    payload = build_payload()

    logger.info("正在发送请求到 %s ...", BASE_URL)
    try:
        response = requests.post(
            BASE_URL,
            json=payload,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        logger.info("请求成功，状态码: %d", response.status_code)
        return response.json()
    except requests.exceptions.Timeout:
        logger.error("请求超时（%d 秒）", DEFAULT_TIMEOUT)
        raise
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP 错误: %s，响应内容: %s", e, response.text)
        raise
    except requests.exceptions.RequestException as e:
        logger.error("请求异常: %s", e)
        raise


if __name__ == "__main__":
    result = run_job()
    print(json.dumps(result, ensure_ascii=False, indent=2))