import requests
import json

url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

headers= {
  "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJoZXJtZXNfYWRtaW5AZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3ODYzNzY2NjY3MCwicHciOiJVTlZQbWM3dCIsImV4cCI6MTc3OTI0MjQ2Nn0.TQ77JD_O8f2_gBJVHCFjvlPpe3FyNlABf98NGEDaFuvGGXXl2ONJl8I3ngcXkOLSAPF_Eqp8QiuMJjbpO2pZsQ",
  "Content-Type": "application/json"
}

payload = json.dumps({
  "dataType": "Weibo",
  "banyanType": "elf",
  "searchType": "User",
  "needReturnFields": "item_id,url",
  "searchCondition": [
    # {
    #   "fieldName": "item_id",
    #   "operation": "eq",
    #   "fieldValue": ["5250047550692533", "5215190427895630"]
    # },
    {
      "fieldName": "update_timestamp",
      "operation": "ltegte",
      "fieldValue": [1735660800000, 1770652799000]
    }
  ],
  "sortCondition": {
    "sortFieldName": "publish_timestamp",
    "order": "desc"
  },
  "timeRange": "1735660800000, 1770652799000"
})


response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
