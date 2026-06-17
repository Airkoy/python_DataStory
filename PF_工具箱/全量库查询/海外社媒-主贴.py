import requests
import json

url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3NjM0ODA2NDg1NywicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NzY5NTI4NjR9.fqDuo-9-0yk5IajA6sXXiHZFizfLUNRXtsnOJGDiwn0YRVGQh9_Yv78_p7zBVipBFOTnMFvLa9md3coafZBp-Q"
}
payload = json.dumps({
    "dataType": "GlobalMedia",
    "banyanType": "elf",
    "searchType": "Post",
    # "needReturnFields": "site_id,site_name,is_sensitive_politics,forum_name",
    "needReturnFields": "forum_name,site_name,forum_id",
    "searchCondition": [
        {"fieldName": "site_id","operation": "eq","fieldValue": ["1244369244"]},  # 1228001 reddit 1244369244 巴哈姆特
        # {"fieldName": "title,content","operation": "mp","fieldValue": ["Endfield|Arknights Endfield|エンドフィールド|엔드필드|엔필|終末地", ""]},
        # {"fieldName": "is_sensitive_politics", "operation": "eq", "fieldValue": ["1"]},
        {"fieldName": "forum_name", "operation": "mp", "fieldValue": ["明日方舟：終末地"]},
        {
            "fieldName": "publish_timestamp",
            "operation": "ltegte",
            "fieldValue": [1713283200000, 1776355199000]  # 2024-04-17 00:00:00 ~ 2026-04-16 23:59:59
        }
    ],
    "sortCondition": {
        "sortFieldName": "publish_timestamp",
        "order": "desc"
    },
    "timeRange": "1713283200000,1776355199000"
})

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
