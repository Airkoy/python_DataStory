import requests
import json

url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3NzI1OTkzMjQ3MSwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3Nzc4NjQ3MzJ9.kV4VlrHXJ-oQyIc8tg6oHkQPqz2nXJiFPMMx2FibeKYN8cwxWwHml439q0t-HJzJjaUb54nWsy2iBLaUxfn_tg"
}

payload = json.dumps({
  "dataType": "Wechat",
  "banyanType": "ork",
  "searchType": "Content",
  "needReturnFields": "item_id,url,title,content",
  "searchCondition": [
    {
      "fieldName": "user_name",
      "operation": "mp",  # eq -> 精准匹配
      "fieldValue": ["深圳"]
    },
    {
      "fieldName": "publish_timestamp",
      "operation": "ltegte",
      "fieldValue": [1735660800000,1777305599000]
    },

  ],
  "sortCondition": {
    "sortFieldName": "publish_timestamp",
    "order": "desc"
  },
  "timeRange": "1735660800000,1777305599000"
})


response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)