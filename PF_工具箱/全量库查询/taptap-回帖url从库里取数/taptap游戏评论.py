import requests
import json
import pandas as pd
import time
import re
from datetime import datetime  # 新增：导入时间处理模块

url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

headers = {
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJoZXJtZXNfYWRtaW5AZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3ODIwNjM0NTUyMiwicHciOiJVTlZQbWM3dCIsImV4cCI6MTc3ODgxMTE0NX0.IMofC8Ioi7BwxIbI-YFx662bH8idSkMaVNswn-DeQvP8MDwP-nHqnbP35anLNcyZjZbeKgYwYDRpaq2Q43cvbw",
    "Content-Type": "application/json",
}


# 清除 Excel 不支持的特殊非法字符的函数
def clean_illegal_chars(text):
    if not isinstance(text, str):
        return text
    # 匹配 XML/Excel 不允许的控制字符并移除
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

# 新增：时间戳转换为 yyyymmddhhmmss 格式的函数
def format_timestamp(ts):
    if not ts:
        return ""
    try:
        # 接口返回的是毫秒级时间戳，需除以1000转为秒级
        dt = datetime.fromtimestamp(int(ts) / 1000)
        return dt.strftime("%Y%m%d%H%M%S")
    except:
        return ""

with open("taptap.json", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"共读取 {len(urls)} 条URL")

BATCH_SIZE = 100
batches = [urls[i:i + BATCH_SIZE] for i in range(0, len(urls), BATCH_SIZE)]
print(f"共分为 {len(batches)} 批次")

all_results = []

for batch_idx, batch_urls in enumerate(batches, start=1):
    payload = json.dumps({
        "dataType": "NewsForum",
        "banyanType": "elf",
        "searchType": "Comment",
        "needReturnFields": "item_id,url,content,like_cnt,comment_cnt,update_timestamp",
        "searchCondition": [
            {
                "fieldName": "url",
                "operation": "eq",
                "fieldValue": batch_urls
            },
            {"fieldName": "site_id", "operation": "eq", "fieldValue": ["1003678"]},
            {"fieldName": "parent_item_id", "operation": "nl", "fieldValue": []},

            {
                "fieldName": "publish_timestamp",
                "operation": "ltegte",
                "fieldValue": [1775664000000, 1778255999999]
            }
        ],
        "sortCondition": {
            "sortFieldName": "publish_timestamp",
            "order": "desc"
        },
        "timeRange": "1775664000000, 1778255999999"
    })

    try:
        response = requests.post(url, headers=headers, data=payload)
        result = response.json()

        if result.get("success") and result.get("data", {}).get("data"):
            items = result["data"]["data"]
            for item in items:
                # 提前提取并处理数值，避免重复计算
                like_cnt = item.get("like_cnt") or 0
                comment_cnt = item.get("comment_cnt") or 0

                all_results.append({
                    "item_id": item.get("item_id", ""),
                    "url": item.get("url", ""),
                    # 修复问题1：清洗非法字符，防止写入Excel报错
                    "content": clean_illegal_chars(item.get("content", "")),
                    # 修复问题2：使用 or 0，将 None 强制转为 0
                    "like_cnt": like_cnt,
                    "comment_cnt": comment_cnt,
                    # 修改：将时间戳格式化为 yyyymmddhhmmss
                    "update_timestamp": format_timestamp(item.get("update_timestamp")),
                    # 新增：互动量 = 点赞数 + 评论数
                    "互动量": like_cnt + comment_cnt,
                })
            print(f"✓ 批次 {batch_idx}/{len(batches)} | 本批 {len(batch_urls)} 条URL -> 获取到 {len(items)} 条记录")
        else:
            print(f"✗ 批次 {batch_idx}/{len(batches)} | 本批 {len(batch_urls)} 条URL -> 无数据返回")

    except Exception as e:
        print(f"✗ 批次 {batch_idx}/{len(batches)} -> 请求异常: {e}")

    time.sleep(0.5)

# 输出到Excel，columns中新增"互动量"
df = pd.DataFrame(all_results,
                  columns=["item_id", "url", "content", "like_cnt", "comment_cnt", "互动量", "update_timestamp"])
df.to_excel("taptap_results.xlsx", index=False)
print(f"\n完成！共获取 {len(all_results)} 条记录，已保存到 taptap_results.xlsx")