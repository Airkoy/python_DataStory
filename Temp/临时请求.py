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
    "appId": 13,
    "exportConfig": {
        "local": {}
    },
    "globalConfig": {
        "email": "koy@datastory.com.cn",
        "emailMode": 2,
        "isKeepTrend": False,
        "isRealTime": {
            "COMMENT": 1,
            "INTERACTION": 1,
            "POST": 0
        }
    },
    "jobName": "小红书-单帖url-不传schedtime-在线",
    "scheduleConfig": {
        "commentDelayList": [
            1,
            2,
            3
        ],
        "commentDelayUnit": "H",
        "endDataTime": 1786118399000,
        "interactionDelayList": [
            1
        ],
        "interactionDelayUnit": "d",
        "interval": 1,
        "postDelay": 0,
        # "schedStartTime": 1783394941341,
        "startDataTime": 1754582400000,
        "type": "SIMPLE",
        "unit": "d",
        "useInteractionDefaultDelay": False
    },
    "scopeId": 11,
    "sheetId": 76552,
    "sourceConfig": {
        "condition": [
            {
                "name": "分析对象1",
                "url": "https://www.xiaohongshu.com/search_result/68ce09d9000000001201c9f6"
            }
        ],
        "fieldMode": 0,
        "input": "surl",
        "isCoproduce": 0,
        "matchType": [],
        "output": [
            "POST",
            "INTERACTION",
            "COMMENT"
        ]
    },
    "submitType": "async"
}

# 发送POST请求
response = requests.post(url, data=json.dumps(requestData), headers=headers)

# 输出响应数据
print(response.text)
