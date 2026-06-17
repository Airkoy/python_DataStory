import json
from elasticsearch import Elasticsearch


def save_output(resp):
    """将 ES 查询结果保存到 result/output.json"""
    output = {
        "total": resp["hits"]["total"]["value"],
        "data": resp["hits"]["hits"]
    }
    with open("../result/output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print("已写入 output.json")


def save_es_query(index_name, query_dict, size, sort=None, aggs=None):
    """将 ES 查询语句保存为 Kibana Dev Tools 格式到 result/es_test.json"""
    es_query_body = {"size": size, "query": query_dict}
    if sort is not None:
        es_query_body["sort"] = sort
    body_str = json.dumps(es_query_body, ensure_ascii=False, indent=2)
    indented_body_str = "\n".join(["  " + line for line in body_str.split("\n")])
    kibana_query_str = f"GET {index_name}/_search\n{indented_body_str}"
    with open("../result/es_test.json", "w", encoding="utf-8") as f:
        f.write(kibana_query_str)
    print("已写入 es_test.json (Kibana Dev Tools 格式，可直接复制使用)")


# 连接 ES
es = Elasticsearch(
    ["https://es-banyan-global.datastory.com.cn"],
    basic_auth=("banyan-custom", "banyan-custom-zxcv"),
    request_timeout=60
)

# ================= 定义查询参数 =================
INDEX_NAME = "ds-banyan-globalmedia-post-index-v3"
QUERY_SIZE = 100

QUERY_DICT = {
        "bool": {
            "must": [
                {
                    "term": {
                        "site_name.raw": {
                            "value": "YouTube",
                        },
                    },
                },
                {
                    "wildcard": {
                        "user_item_url": {
                            "value": "https://www.youtube.com/@*",
                        },
                    },
                },
            ],
            "must_not": [
                {
                    "wildcard": {
                        "user_item_url": {
                            "value": "https://www.youtube.com/channel*",
                        },
                    },
                },
            ],
        },
    }

# ================= 执行查询 =================
resp = es.search(
    index=INDEX_NAME,
    size=QUERY_SIZE,
    query=QUERY_DICT,
)

# ================= 输出结果 =================
save_output(resp)
save_es_query(INDEX_NAME, QUERY_DICT, QUERY_SIZE)