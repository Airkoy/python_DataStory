import os
import requests
import json

url = 'https://dc.datastory.com.cn/application/market/job/v1/run'
# url = "https://dc.datastory.com.cn/application/market/plugin/job/run" # 自定义站点

headers = {
  "Content-Type": "application/json",
  "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc4NjAxNzI2OTU5MCwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3ODY2MjIwNjl9.KpZMzfQv0QdxZherzd_RCSLiboXmzpqZOlJj1TjO5yfxAeE_--R0SlzAicwUlduZ-D8iF3goxBz1xzTd92ho-Q"
}

requestData = {
    "appId": 12,
    "exportConfig": {
        "local": {}
    },
    "globalConfig": {
        "email": "koy@datastory.com.cn",
        "emailMode": 2,
        "isKeepTrend": False,
        "isRealTime": {
            "POST": 0
        }
    },
    "jobName": "测试-api创建-重名文件夹",
    "scheduleConfig": {
        "endDataTime": 1783908791964,
        "interactionDelayUnit": "d",
        "postDelay": 0,
        "schedStartTime": 1783908851964,
        "startDataTime": 1752459191964,
        "type": "TEMP",
        "useInteractionDefaultDelay": False
    },
    "scopeId": 6,
    # "sheetId": 76552,
    "sheetName":"20260806版本测试",
    "sourceConfig": {
        "condition": [
            {
                "filterwords": "",
                "keywords": "新品上市|全新上市|重磅上市",
                "name": "分析对象1",
                "uid": "2918373202"
            }
        ],
        "fieldMode": 0,
        "input": "uid",
        "isCoproduce": 0,
        "matchType": [
            "content",
            "title"
        ],
        "output": [
            "POST-video#0",
            "POST-image#0"
        ]
    }
}

# 发送POST请求
response = requests.post(url, data=json.dumps(requestData), headers=headers)

# 输出响应数据
print(response.text)
