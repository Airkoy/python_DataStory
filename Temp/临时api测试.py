import json

import requests

url = "http://api.dc.datastory.com.cn/api/socialmedia/totalVolume"
site_ids = [
    "44", "47", "32", "35", "36", "40", "129472", "129478",
    "137895", "25053073", "25053070"
]

payload = {
    "token": "e7a4685c941137c475817a8110998fc0",
    "sources": ["video"],
    "sentiments": [1, 0, -1],
    "keyword": "that",
    "startTime": "1767283199000",
    "endTime": "1782921599000",
    "extra_condition": {"video": {"siteIds": ""}}
}
headers = {
    "Content-Type": "application/json",
    "Cookie": "sl-session=V8AiYBv0WmpCZis+5mfWIw=="
}

for site_id in site_ids:
    payload["extra_condition"]["video"]["siteIds"] = site_id
    print(f"\n{'=' * 20} site_id: {site_id} {'=' * 20}")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        try:
            print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        except requests.exceptions.JSONDecodeError:
            print(response.text)
    except requests.RequestException as exc:
        print(f"请求失败：{exc}")
