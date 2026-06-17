import requests
import json

url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3NDM0Mzc1MTAxMSwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NzQ5NDg1NTF9.6TZnKm4hfWBnqhjIFAYu55c-vBQjeay6xaHtazW30gFnDMOksbJ6HpdK-tS3R7SCZVZWze4UOSerFkFuO1t6bw"
}

payload = json.dumps({
    "dataType": "GlobalMedia",
    "banyanType": "elf",
    "searchType": "User",
    "needReturnFields": "item_id,item_url,update_timestamp",
    "searchCondition": [
        {
            "fieldName": "item_id",
            "operation": "eq",  # eq -> 精准匹配
            "fieldValue": [
                "@tencentvideo",
                "@tencentvideominidrama",
                "@tencentvideodrama",
                "@tencentvideosuspense",
                "@tencentvideoromantic",
                "@tencentvideocostume",
                "@wetvvietnam",
                "@wetvtaiwanofficial",
                "@tencentvideoartist"
            ]

        },
        {
            "fieldName": "site_name",
            "operation": "mp",  # eq -> 精准匹配
            "fieldValue": ["youtube", ""]
        },
        {
            "fieldName": "update_timestamp",
            "operation": "ltegte",
            "fieldValue": [1771948800000, 1774367999999]
        },

    ],
    "sortCondition": {
        "sortFieldName": "publish_timestamp",
        "order": "desc"
    },
    "timeRange": "1771948800000,1774367999999"
})

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)