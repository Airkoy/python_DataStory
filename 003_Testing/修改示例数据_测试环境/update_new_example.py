"""
测试环境 - 保存新示例数据接口
POST http://dc.dev.datastory.com.cn/app/demo/save

功能：向测试环境提交新的示例数据（微博帖子），用于 DataStory 平台的 Demo 展示。
"""
import json
from pathlib import Path

import pandas as pd
import requests

# ---- 常量 ----
# Excel 文件路径（相对于本脚本所在目录）
EXCEL_FILE = Path(__file__).resolve().parent / "微博_主贴示例数据.xlsx"


def build_payload() -> dict:
    """
    从 Excel 文件中读取列名和数据行，构建请求体。

    Excel 要求：
      - 第一行为列名（与接口 columns 字段对应）
      - 后续每行为一条数据记录

    :return: 包含 appId, output, columns, json 的字典
    """
    df = pd.read_excel(EXCEL_FILE, dtype=str)

    # 列名列表
    columns = df.columns.tolist()

    # 将 NaN 替换为空字符串，再转为字典列表
    df = df.where(df.notna(), "")
    rows = df.to_dict(orient="records")

    print(f"从 Excel 读取到 {len(rows)} 行数据，{len(columns)} 个字段。")

    return {
        "appId": "6",
        "output": "4_POST",
        "columns": json.dumps(columns, ensure_ascii=False),
        "json": json.dumps(rows, ensure_ascii=False),
    }


def save_new_example() -> dict:
    """
    调用测试环境「保存新示例数据」接口。

    :return: 接口返回的 JSON 数据
    :raises AccountError: 账号不存在或凭据不完整
    :raises TokenError: Token 获取失败
    :raises requests.RequestException: 网络请求异常
    """
    # 1. 获取认证 Token
    url = 'http://dc.dev.datastory.com.cn/auth/obtain'
    data = {
        "username": "hermes_admin@datastory.com.cn",
        "password": "123456",  # 测试环境
    }
    response = requests.post(url, data=data)

    # 直接提取token并构建headers
    token = response.json()['data']
    headers = {
        "Content-Type": 'application/json',
        'Authorization': token,
    }


    # 2. 构建请求体
    payload = build_payload()

    print(f"正在发送请求到  ...")
    print(f"数据行数: {len(json.loads(payload['json']))}")

    # 3. 发送 POST 请求
    SAVE_URL = "http://dc.dev.datastory.com.cn/app/demo/save"
    response = requests.post(
        SAVE_URL,
        json=payload,
        headers=headers,
        timeout=60,
    )
    response.raise_for_status()

    print(f"请求成功，状态码: {response.status_code}")
    return response.json()


# --- 主程序入口 ---
if __name__ == "__main__":
    try:
        result = save_new_example()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except requests.exceptions.Timeout:
        print(f"\n❌ 请求超时（{60} 秒）")
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP 错误: {e}")
        if e.response is not None:
            print(f"响应内容: {e.response.text[:500]}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 网络请求异常: {e}")
    except Exception as e:
        print(f"\n❌ 发生未知错误: {e}")
