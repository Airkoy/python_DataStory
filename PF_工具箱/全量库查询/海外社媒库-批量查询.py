import requests
import json
import pandas as pd
from datetime import datetime
import time

# 站点ID映射表
site_id_map = {
    "1202847": "ins",
    "1244193084": "YouTube",
    "1228001": "reddit",
    "1227422": "facebook",
    "1244369240": "Dcinside",
    "1244369241": "Ruliweb",
    "1244369242": "Arclive",
    "24197157": "steam_游戏",
    "1244924692": "steam_社区",
    "1244369244": "巴哈姆特",
    "1244734557": "INVEN_新闻",
    "1244369437": "naver_game",
    "1244369245": "5ch",
    "1244098518": "naver_cafe",
    "1244369436": "Pinterest",
    "1244734558": "INVEN_论坛",
    "1244369434": "TIKTOK",
    "1244070317": "X"
}

# 配置参数
url = "https://dc.datastory.com.cn/banyan/searchInBanyan"
headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3NjM0ODA2NDg1NywicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NzY5NTI4NjR9.fqDuo-9-0yk5IajA6sXXiHZFizfLUNRXtsnOJGDiwn0YRVGQh9_Yv78_p7zBVipBFOTnMFvLa9md3coafZBp-Q"
}

# 时间范围：2024-04-17 00:00:00 ~ 2026-04-16 23:59:59
start_time = 1713283200000  # 2024-04-17 00:00:00
end_time = 1776355199000  # 2026-04-16 23:59:59
time_range_str = f"{datetime.fromtimestamp(start_time / 1000).strftime('%Y-%m-%d')} ~ {datetime.fromtimestamp(end_time / 1000).strftime('%Y-%m-%d')}"

# 关键词
keywords = "Endfield|Arknights Endfield|エンドフィールド|엔드필드|엔필|終末地"


# 发送请求的函数
def send_request(site_id, is_sensitive_politics):
    payload = {
        "dataType": "GlobalMedia",
        "banyanType": "elf",
        "searchType": "Post",
        "needReturnFields": "site_id,site_name,is_sensitive_politics",
        "searchCondition": [
            {
                "fieldName": "site_id",
                "operation": "eq",
                "fieldValue": [site_id]
            },
            {
                "fieldName": "title,content",
                "operation": "mp",
                "fieldValue": [keywords, ""]
            },
            {
                "fieldName": "is_sensitive_politics",
                "operation": "eq",
                "fieldValue": [str(is_sensitive_politics)]
            },
            {
                "fieldName": "publish_timestamp",
                "operation": "ltegte",
                "fieldValue": [start_time, end_time]
            }
        ],
        "sortCondition": {
            "sortFieldName": "publish_timestamp",
            "order": "desc"
        },
        "timeRange": f"{start_time},{end_time}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get('success') and result.get('data'):
                return result['data'].get('total', 0)
            else:
                return f"API错误: {result.get('message', '未知错误')}"
        else:
            return f"HTTP {response.status_code}"
    except Exception as e:
        return f"请求失败: {str(e)}"


# 主函数
def main():
    results = []

    # 遍历所有site_id
    for site_id, site_name in site_id_map.items():
        print(f"正在查询: {site_name} ({site_id})")

        # 查询 is_sensitive_politics = 0
        print(f"  - is_sensitive_politics = 0")
        total_0 = send_request(site_id, 0)
        results.append({
            '站点名称': site_name,
            '查询时间范围': time_range_str,
            '关键词': keywords,
            'is_sensitive_politics': 0,
            'total': total_0
        })

        # 查询 is_sensitive_politics = 1
        print(f"  - is_sensitive_politics = 1")
        total_1 = send_request(site_id, 1)
        results.append({
            '站点名称': site_name,
            '查询时间范围': time_range_str,
            '关键词': keywords,
            'is_sensitive_politics': 1,
            'total': total_1
        })

        # 避免请求过快
        time.sleep(1)

    # 创建DataFrame
    df = pd.DataFrame(results)

    # 保存为Excel文件
    output_file = '关键词全量库查询结果.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"\n{'=' * 50}")
    print(f"查询完成！结果已保存到 {output_file}")
    print(f"共查询 {len(site_id_map)} 个站点，{len(results)} 条记录")
    print(f"{'=' * 50}")

    # 打印汇总信息
    print("\n查询结果汇总:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()