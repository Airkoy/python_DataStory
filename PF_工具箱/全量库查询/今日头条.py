import requests
import json
import pandas as pd
from datetime import datetime

# === 1. 发送请求（你的原始代码）===
url = "https://dc.datastory.com.cn/banyan/searchInBanyan"
headers = {
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc2ODgwMTYwMzc4NywicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3Njk0MDY0MDN9.qn4w6W-2v_FOg9YyeXofVNPPODdtduqw0OluzkIwOYeqmKsvjfH8wb3pOdYxsS6_473yBEhbPtCwPh_IXqTbKg",
    "Content-Type": "application/json"
}
payload = json.dumps({
    "dataType": "NewsForum",
    "banyanType": "elf",
    "searchType": "Post",
    "needReturnFields": "url,pic_urls,post_type,update_timestamp",
    "searchCondition": [
        {"fieldName": "site_id", "operation": "eq", "fieldValue": ["1001569"]},
        # {"fieldName": "post_type", "operation": "eq", "fieldValue": ["32833"]},
        {"fieldName": "url", "operation": "nn", "fieldValue": []},
        {"fieldName": "publish_timestamp", "operation": "ltegte", "fieldValue": [1766160000000, 1768838399999]},
    ],
    "sortCondition": {"sortFieldName": "publish_timestamp", "order": "desc"},
    "timeRange": "1737343635000,1768879635000"
})

response = requests.post(url, headers=headers, data=payload)

# === 2. 解析 JSON ===
try:
    result = response.json()
except Exception as e:
    print("❌ JSON 解析失败:", e)
    print("响应内容:", response.text[:500])
    exit()

if not result.get("success"):
    print("❌ API 返回失败:", result.get("message"))
    exit()

records = result["data"]["data"]  # 这就是你要的列表

# === 3. 预处理：时间戳转可读时间（可选）===
def ts_to_str(ts):
    if ts is None:
        return ""
    try:
        return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ts)

for rec in records:
    rec["update_time"] = ts_to_str(rec.get("update_timestamp"))

# === 4. 转 DataFrame 并保存 ===
df = pd.DataFrame(records)

# 指定列顺序（可选，让 Excel 更整洁）
columns_order = ["url", "post_type", "update_timestamp", "update_time", "pic_urls"]
# 过滤存在的列
columns_order = [col for col in columns_order if col in df.columns]

df = df[columns_order]

# 保存到 Excel
output_file = "头条监控帖子数据3.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ 成功导出 {len(df)} 条记录到 '{output_file}'")