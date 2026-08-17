import os
import requests
import json

# url = 'http://dc.dev.datastory.com.cn/application/market/job/v1/run'
url = 'https://dc.datastory.com.cn/application/market/job/v1/run'

headers = {
    "Content-Type": "application/json",
    "Authorization": os.environ["DATASTORY_AUTHORIZATION"]
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
    "jobName": "X关键词国家0608新-re-不传postdelay",

    "scheduleConfig": {
        "endDataTime": 1779760854000,
        "interactionDelayUnit": "d",
        # "postDelay": 0,
        "schedStartTime": 1780897834510,
        "startDataTime": 1779674454000,
        "type": "TEMP",
        "useInteractionDefaultDelay": False
    },
    "scopeId": 105,
    "sheetName": "0625临时",
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
