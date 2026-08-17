import os
import requests
import json

# query_task_dev = "http://dc.dev.datastory.com.cn/application/market/job/v1/detail?id=47969"
query_task_prod = "https://dc.datastory.com.cn/application/market/job/v1/detail?id=14405826&uuu=banyan"
headers = {
  "Content-Type": "application/json",
  "Authorization": os.environ["DATASTORY_AUTHORIZATION"]
}

response = requests.request("GET", query_task_prod, headers=headers)
response_data = response.json()
# print(response.text)
print(response_data)

# "scheduleConfig":{"type":"TEMP","schedStartTime":"1774005037327","interactionDelayUnit":"d","useInteractionDefaultDelay":false,"postDelay":0.0}

# new_requestData = response_data['data']
# new_requestData['exportConfig'] = export_config
# new_requestData['sheetId'] = sheet_id
# new_requestData["workflowId"] = ''
