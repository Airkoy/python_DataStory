import requests
import json

url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc2NTUzMjg1NjU5OSwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NjYxMzc2NTZ9.dkZQUdPjAvN0w-XsyN-ZizGHox69SkaI_3tfbzH1WbKRPvxzSRFQvTUbQxrMHkjAFLi4oOMjwyIiOM1ih1wiGA',
  'Cookie': 'dc-login-iden=.datastory.com.cn#e3279c4f-42cd-4195-9410-15efa172e134; SESSION=4aa8a18b-f80a-4fa4-b4e6-026514bdcea3'
}

payload = json.dumps({
  "dataType": "NewsForum",
  "banyanType": "elf",
  "searchType": "Post",
  "needReturnFields": "site_name,site_id,post_type,update_timestamp",
  "searchCondition": [
    {
      "fieldName": "site_id",
      "operation": "eq",  # eq -> 精准匹配
      "fieldValue": ["101944"]
    },
    {
      "fieldName": "post_type",
      "operation": "eq",
      "fieldValue": ["video_car"]
    },
    {
      "fieldName": "site_source_ids",
      "operation": "ne",
      "fieldValue": ["101944"]
    },
    {
      "fieldName": "publish_timestamp",
      "operation": "ltegte",
      "fieldValue": [1735660800000, 1765727999000]
    },

  ],
  "sortCondition": {
    "sortFieldName": "publish_timestamp",
    "order": "desc"
  },
  "timeRange": "1735660800000,1765382399000"
})


response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
