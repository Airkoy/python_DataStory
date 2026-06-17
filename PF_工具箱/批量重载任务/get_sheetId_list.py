import requests
import json

url_test_datamarket = "http://dc.dev.datastory.com.cn/sheet/list?uuu=banyan"

headers= {
  "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc3MzgyNjYxNTA4NiwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NzQ0MzE0MTV9.eS58vpPHtV7VFp6RiSTv4NNI7o1uGaO5kzl3aa4FUE-MxPFj3SpnS3s0P0Ot65hYJEqmDLK4ENgLfYiFFQFqhg",
  "Content-Type": "application/json"
}

response = requests.request("GET", url_test_datamarket, headers=headers)
response_data = response.json()
print(response.text)