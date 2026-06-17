import requests
import json

url = 'http://dc.dev.datastory.com.cn/application/market/job/v1/run'
headers = {
  "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc4MTA3Mjk2OTk1NSwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3ODE2Nzc3Njl9.RQ4ptgyW1ytoUGSv_Y1A6yI4-adijnZOf81fAQA8mSco9IXslrkBzipPibVtWzLO2B9vgKz-xUX8jz6F36Eqxw",
  "Content-Type": "application/json"
}

# 构建请求体数据
requestData = {
    "appId": 121,
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
    "jobName": "X关键词国家0608新",
    "reloadJobId": 54459,
    "scheduleConfig": {
        "endDataTime": 1779760854000,
        "interactionDelayUnit": "d",
        "postDelay": 0,
        "schedStartTime": 1780897834510,
        "startDataTime": 1779674454000,
        "type": "TEMP",
        "useInteractionDefaultDelay": False
    },
    "scopeId": 105,
    "sheetName": "测试文件夹名",
    "sourceConfig": {
        "condition": [
            {
                "countries_ori": "美澳大利亚",
                "filterwords": "",
                "keywords": "this+that+cool",
                "name": "分析对象1"
            }
        ],
        "fieldMode": 0,
        "input": "keyword",
        "isCoproduce": 0,
        "matchType": [
            "content",
            "title"
        ],
        "output": [
            "POST"
        ]
    },

}

# 发送POST请求
response = requests.post(url, data=json.dumps(requestData), headers=headers)

# 输出响应数据
print(response.text)