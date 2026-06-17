import requests
import json

query_task_dev = "http://dc.dev.datastory.com.cn/application/market/job/v1/detail?id=47969"
# query_task_prod = "https://dc.datastory.com.cn/application/market/job/v1/detail?id=47969&uuu=banyan"

headers = {
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3NDUxOTc5MTk3OSwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NzUxMjQ1OTF9.K6vHOs2Sllu_eF0rFrx8FYXI2XfFMV04zCKCJN4M4_0juLYY0_36MBS8gk8_QDUCMoLGmL-idnh8roqe20Cf1Q",
    "Content-Type": "application/json"
}

response = requests.request("GET", query_task_dev, headers=headers)
response_data = response.json()
# print(response.text)
print(response_data['data']['scheduleConfig'])

# "scheduleConfig":{"type":"TEMP","schedStartTime":"1774005037327","interactionDelayUnit":"d","useInteractionDefaultDelay":false,"postDelay":0.0}

# new_requestData = response_data['data']
# new_requestData['exportConfig'] = export_config
# new_requestData['sheetId'] = sheet_id
# new_requestData["workflowId"] = ''
