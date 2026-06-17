import json
import sys
import os
import re


def parse_kibana_query(filepath):
    """
    解析 Kibana Dev Tools 风格的查询文件，格式：
    第一行: GET <index_name>/_search
    后续行: JSON body
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.strip().split("\n")
    first_line = lines[0].strip()
    body_lines = "\n".join(lines[1:])

    m = re.match(r"^GET\s+(.+)/_search$", first_line)
    if not m:
        raise ValueError(f"无法解析第一行 GET 语句: {first_line}")

    index_str = m.group(1).strip()
    index_name = index_str if "," not in index_str else [idx.strip() for idx in index_str.split(",")]

    body = json.loads(body_lines)

    return index_name, body


def format_python_value(value, indent=0):
    """将 Python 值格式化为代码字符串"""
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        if not value:
            return "[]"
        items = [format_python_value(v, indent + 1) for v in value]
        item_str = ", ".join(items)
        if all(len(it) < 40 for it in items) and len(item_str) < 80:
            return f"[{item_str}]"
        inner_indent = "    " * (indent + 1)
        close_indent = "    " * indent
        lines = [f"{inner_indent}{it}," for it in items]
        return "[\n" + "\n".join(lines) + f"\n{close_indent}]"
    if isinstance(value, dict):
        if not value:
            return "{}"
        inner_indent = "    " * (indent + 1)
        close_indent = "    " * indent
        lines = []
        for k, v in value.items():
            v_str = format_python_value(v, indent + 1)
            lines.append(f'{inner_indent}{json.dumps(k, ensure_ascii=False)}: {v_str},')
        return "{\n" + "\n".join(lines) + f"\n{close_indent}}}"
    return json.dumps(value, ensure_ascii=False)


def generate_py_file(index_name, body, output_path):
    size = body.get("size", 0)
    query_dict = body.get("query", {})
    agg_dict = body.get("aggs", None)
    sort_dict = body.get("sort", None)

    has_aggs = agg_dict is not None
    has_sort = sort_dict is not None
    has_hits = size > 0

    index_str = format_python_value(index_name)
    query_str = format_python_value(query_dict, indent=1)
    agg_str = format_python_value(agg_dict, indent=1) if has_aggs else "{}"
    sort_str = format_python_value(sort_dict, indent=1) if has_sort else ""

    lines = []
    lines.append("import json")
    lines.append("from elasticsearch import Elasticsearch")
    lines.append("")
    lines.append("")
    lines.append("def save_output(resp):")
    lines.append('    """将 ES 查询结果保存到 result/output.json"""')
    if has_hits:
        lines.append('    sources = [hit["_source"] for hit in resp["hits"]["hits"]]')
    lines.append("    output = {")
    lines.append('        "total": resp["hits"]["total"]["value"],')
    if has_hits:
        lines.append('        "count": len(sources),')
        lines.append('        "data": sources,')
    if has_aggs:
        lines.append('        "aggregations": resp["aggregations"],')
    lines.append("    }")
    lines.append('    with open("../result/output.json", "w", encoding="utf-8") as f:')
    lines.append("        json.dump(output, f, ensure_ascii=False, indent=4)")
    if has_hits:
        lines.append('    print(f"已写入 output.json，共 {len(sources)} 条记录")')
    else:
        lines.append('    print("已写入 output.json")')
    lines.append("")
    lines.append("")
    lines.append("def save_es_query(index_name, query_dict, size, sort=None, aggs=None):")
    lines.append('    """将 ES 查询语句保存为 Kibana Dev Tools 格式到 result/es_test.json"""')
    lines.append('    es_query_body = {"size": size, "query": query_dict}')
    if has_aggs:
        lines.append("    if aggs is not None:")
        lines.append('        es_query_body["aggs"] = aggs')
    lines.append("    if sort is not None:")
    lines.append('        es_query_body["sort"] = sort')
    lines.append('    body_str = json.dumps(es_query_body, ensure_ascii=False, indent=2)')
    lines.append('    indented_body_str = "\\n".join(["  " + line for line in body_str.split("\\n")])')
    lines.append('    kibana_query_str = f"GET {index_name}/_search\\n{indented_body_str}"')
    lines.append('    with open("../result/es_test.json", "w", encoding="utf-8") as f:')
    lines.append("        f.write(kibana_query_str)")
    lines.append('    print("已写入 es_test.json (Kibana Dev Tools 格式，可直接复制使用)")')
    lines.append("")
    lines.append("")
    lines.append("# 连接 ES")
    lines.append("es = Elasticsearch(")
    lines.append('    ["https://es-banyan-global.datastory.com.cn"],')
    lines.append('    basic_auth=("banyan-custom", "banyan-custom-zxcv"),')
    lines.append("    request_timeout=60")
    lines.append(")")
    lines.append("")
    lines.append("# ================= 定义查询参数 =================")
    lines.append(f"INDEX_NAME = {index_str}")
    lines.append(f"QUERY_SIZE = {size}")
    if has_sort:
        lines.append(f"QUERY_SORT = {sort_str}")
    lines.append("")
    lines.append(f"QUERY_DICT = {query_str}")
    if has_aggs:
        lines.append("")
        lines.append(f"AGG_DICT = {agg_str}")
    lines.append("")
    lines.append("# ================= 执行查询 =================")
    lines.append("resp = es.search(")
    lines.append("    index=INDEX_NAME,")
    lines.append("    size=QUERY_SIZE,")
    if has_sort:
        lines.append("    sort=QUERY_SORT,")
    lines.append("    query=QUERY_DICT,")
    if has_aggs:
        lines.append("    aggregations=AGG_DICT,")
    lines.append(")")
    lines.append("")

    lines.append("# ================= 输出结果 =================")
    lines.append("save_output(resp)")
    if has_aggs and has_sort:
        lines.append("save_es_query(INDEX_NAME, QUERY_DICT, QUERY_SIZE, sort=QUERY_SORT, aggs=AGG_DICT)")
    elif has_aggs:
        lines.append("save_es_query(INDEX_NAME, QUERY_DICT, QUERY_SIZE, aggs=AGG_DICT)")
    elif has_sort:
        lines.append("save_es_query(INDEX_NAME, QUERY_DICT, QUERY_SIZE, sort=QUERY_SORT)")
    else:
        lines.append("save_es_query(INDEX_NAME, QUERY_DICT, QUERY_SIZE)")

    content = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"已生成: {output_path}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # print(script_dir)
    # print(os.path.abspath(__file__))
    default_input = os.path.join(script_dir, "es_query.json")
    default_output = os.path.join(script_dir, "数据问题查询/赞助商_合作品牌需求.py")

    input_path = sys.argv[1] if len(sys.argv) > 1 else default_input
    output_path = sys.argv[2] if len(sys.argv) > 2 else default_output

    if not os.path.exists(input_path):
        print(f"错误: 输入文件不存在: {input_path}")
        sys.exit(1)

    index_name, body = parse_kibana_query(input_path)
    generate_py_file(index_name, body, output_path)


if __name__ == "__main__":
    main()
