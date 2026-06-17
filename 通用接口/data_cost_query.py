"""
查询用户交易数据成本（DataCost）接口。

接口说明：
    POST https://dc.datastory.com.cn/user/transaction/dataCost?uuu=banyan
    Content-Type: application/x-www-form-urlencoded

使用方式：
    python data_cost_query.py
"""
import json
import sys
from pathlib import Path

# 确保能导入同目录下的 auto_get_token 模块
sys.path.insert(0, str(Path(__file__).parent))

import requests
from auto_get_token import TokenManager, AccountError, TokenError

# [1781107200000, 1781107200000]
def query_transaction_data_cost(
    account_name: str = "admin账号",
    uuu: str = "banyan",
    start_time: str = "1781679600000",
    end_time: str = "1781107200000",
    search_type: str = "account",
    keyword: str = "meiling.zhou@shangri-la.com",
    email: str = "",
    compute: str = "job",
    page: int = 1,
    size: int = 10,
):
    """
    查询用户交易数据成本。

    :param account_name: 账号名称，对应 accounts.json 中的 key
    :param uuu: URL 查询参数 uuu
    :param start_time: 开始时间（毫秒级时间戳）
    :param end_time: 结束时间（毫秒级时间戳）
    :param search_type: 搜索类型
    :param keyword: 关键词
    :param email: 邮箱
    :param compute: 计算类型
    :param page: 页码
    :param size: 每页条数
    :return: 接口返回的 JSON 数据，失败返回 None
    """
    # 初始化 TokenManager
    token_manager = TokenManager()

    # 获取认证请求头
    try:
        headers = token_manager.get_headers(account_name)
    except (AccountError, TokenError) as e:
        print(f"❌ 认证失败: {e}")
        return None

    # 覆盖 Content-Type 为 form-urlencoded
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    # 请求 URL 与查询参数
    url = "https://dc.datastory.com.cn/user/transaction/dataCost"
    params = {"uuu": uuu}

    # 表单数据
    data = {
        "startTime": start_time,
        "endTime": end_time,
        "searchType": search_type,
        "keyword": keyword,
        "email": email,
        "compute": compute,
        "page": str(page),
        "size": str(size),
    }

    # 发送 POST 请求
    try:
        response = requests.post(
            url,
            params=params,
            headers=headers,
            data=data,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        print("✅ 请求成功！")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误: {e}")
        if e.response is not None:
            print(f"   状态码: {e.response.status_code}")
            print(f"   响应内容: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
    except json.JSONDecodeError:
        print("❌ 响应内容不是有效的 JSON")

    return None


if __name__ == "__main__":
    query_transaction_data_cost()
