import json
from elasticsearch import Elasticsearch


def save_output(resp):
    """将 ES 查询结果保存到 result/output.json"""
    sources = [hit["_source"] for hit in resp["hits"]["hits"]]
    output = {
        "total": resp["hits"]["total"]["value"],
        "count": len(sources),
        "data": sources,
        "aggregations": resp["aggregations"],
    }
    with open("../result/output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"已写入 output.json，共 {len(sources)} 条记录")


def save_es_query(index_name, query_dict, size, sort=None, aggs=None):
    """将 ES 查询语句保存为 Kibana Dev Tools 格式到 result/es_test.json"""
    es_query_body = {"size": size, "query": query_dict}
    if aggs is not None:
        es_query_body["aggs"] = aggs
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
INDEX_NAME = [
    "ds-banyan-globalmedia-post-index-v3",
    "ds-banyan-globalnewsforum-post-index-v3",
    "ds-banyan-twitter-post-index-v3",
    "ds-banyan-tiktok-post-index-v3",
]
QUERY_SIZE = 10

QUERY_DICT = {
    "bool": {
        "must": [
            {"terms": {"site_id": ["1244193084", "1227422", "1202847", "1228001","1244369434","1244070317"]}}
            # {"terms": {"site_id": ["1244193084"]}}
        ]
    }
}

AGG_DICT = {
        "by_site_name": {
            "terms": {
                "field": "site_name.raw",
                "size": 100,
            },
            "aggs": {
                "by_verifiedtype": {
                    "terms": {
                        "field": "user_verified_type",
                        "size": 100,
                    },
                },
                "by_accounttype": {
                    "terms": {
                        "field": "account_type",
                        "size": 10,
                    },
                },
                "by_isverified": {
                    "terms": {
                        "field": "is_verified",
                        "size": 10,
                    },
                },
            },
        },
    }

# ================= 执行查询 =================
resp = es.search(
    index=INDEX_NAME,
    size=QUERY_SIZE,
    query=QUERY_DICT,
    aggregations=AGG_DICT,
)

# ================= 输出结果 =================
save_output(resp)
save_es_query(INDEX_NAME, QUERY_DICT, QUERY_SIZE, aggs=AGG_DICT)