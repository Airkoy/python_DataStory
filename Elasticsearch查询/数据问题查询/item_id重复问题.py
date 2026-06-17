import json
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ["https://es-banyan-global.datastory.com.cn"],
    basic_auth=("banyan-custom", "banyan-custom-zxcv"),
    request_timeout=60
)

INDEX_NAME = "ds-banyan-globalmedia-post-index-v3"
QUERY_SIZE = 0

QUERY_DICT = {
    "bool": {
        "must": [
            # {"terms": {"site_id": ["1244193084", "1227422", "1202847", "1228001"]}}
            {"terms": {"site_id": ["1244193084"]}}
        ]
    }
}

AGG_DICT = {
    "by_site_NAME": {
        "terms": {
            "field": "site_name.raw",
            "size": 10
        },
        "aggs": {
            "duplicate_item_ids": {
                "terms": {
                    "field": "item_id",
                    "min_doc_count": 2,
                    "size": 100
                }
            }
        }
    }
}

resp = es.search(
    index=INDEX_NAME,
    size=QUERY_SIZE,
    query=QUERY_DICT,
    aggregations=AGG_DICT
)

output = {
    "total": resp["hits"]["total"]["value"],
    "aggregations": resp["aggregations"]
}

with open("../result/output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print("已写入 output.json")

# 1. 组装 ES Request Body (不包含索引名，索引名放在 GET 后面)
es_query_body = {
    "size": QUERY_SIZE,
    "query": QUERY_DICT,
    "aggs": AGG_DICT
}

# 2. 将 body 转为格式化的 JSON 字符串
body_str = json.dumps(es_query_body, ensure_ascii=False, indent=2)

# 3. 将 JSON body 的每一行增加2个空格缩进，使其符合 Kibana 的美观排版风格
indented_body_str = "\n".join(["  " + line for line in body_str.split("\n")])

# 4. 拼接 Kibana Dev Tools 风格的完整语句
kibana_query_str = f"GET {INDEX_NAME}/_search\n{indented_body_str}"

# 5. 写入文件 (注意：这里写入的是纯文本，不是标准 JSON 对象)
with open("../result/es_test.json", "w", encoding="utf-8") as f:
    f.write(kibana_query_str)

print("已写入 es_test.json (Kibana Dev Tools 格式，可直接复制使用)")
