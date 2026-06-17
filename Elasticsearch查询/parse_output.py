#!/usr/bin/env python3
"""
解析 Elasticsearch 查询结果 output.json，输出 CSV 文件。

用法:
    python parse_output.py
    然后按提示输入 output.json 的路径。
"""

import csv
import json
import sys
from pathlib import Path

# ============================================================
# 可配置：数据记录 CSV 要导出的字段（按顺序）
# ============================================================
DATA_FIELDS = [
    "item_id",
    "user_item_id",
    "user_name",
    "site_name",
    "publish_date_date",
    "publish_date_hour",
    "language",
    "sentiment",
    "like_cnt",
    "comment_cnt",
    "interaction_cnt",
    "content_len",
    "has_pic",
    "is_robot",
    "is_sensitive_politics",
    "is_sensitive_vice",
    "cat_id",
    "url",
    "fingerprint",
    "id",
]


# ============================================================
# 聚合展平（递归，自动适配任意嵌套层级与维度名）
# ============================================================

def _is_agg(obj):
    """判断一个对象是否为 ES 聚合节点（包含 buckets 的 dict）。"""
    return isinstance(obj, dict) and "buckets" in obj


def _flatten_recursive(agg_obj: dict, prefix_row: dict = None, depth: int = 0) -> list[dict]:
    """
    递归展平 ES 嵌套聚合。

    agg_obj 形如:
        {"NAME": {"buckets": [
            {"key": "TikTok", "doc_count": N,
             "NAME": {"buckets": [{"key": "ID", "doc_count": M}]}}
        ]}}

    输出列名自动生成为: 维度1(<agg_name>), 文档数1, 维度2(<agg_name>), 文档数2, ...
    """
    if prefix_row is None:
        prefix_row = {}

    rows = []
    for agg_name, agg_value in agg_obj.items():
        if not _is_agg(agg_value):
            continue
        buckets = agg_value.get("buckets", [])
        level = depth + 1
        key_col = f"维度{level}({agg_name})"
        doc_col = f"文档数{level}"

        for bucket in buckets:
            row = {**prefix_row}
            row[key_col] = bucket.get("key", "")
            row[doc_col] = bucket.get("doc_count", 0)

            # 查找当前 bucket 内的下层聚合
            nested_aggs = {k: v for k, v in bucket.items() if _is_agg(v)}
            expanded = False
            if nested_aggs:
                for nak, nav in nested_aggs.items():
                    if nav.get("buckets"):
                        rows.extend(_flatten_recursive({nak: nav}, row, depth + 1))
                        expanded = True
            if not expanded:
                rows.append(row)

    return rows


def flatten_aggregations(aggregations: dict) -> tuple[list[str], list[dict]]:
    """
    入口：解析 aggregations 区块，返回 (fieldnames, rows)。

    自动发现聚合层级与维度名，无须硬编码。
    """
    rows = _flatten_recursive(aggregations)
    if not rows:
        return [], []

    # 从首行提取列名，保持展平顺序
    fieldnames = list(rows[0].keys())
    return fieldnames, rows


# ============================================================
# CSV 输出
# ============================================================

def write_csv(filepath: str, fieldnames: list[str], rows: list[dict]):
    """写入 CSV 文件（UTF-8 with BOM，兼容 Excel 中文显示）。"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  -> 已输出: {filepath} ({len(rows)} 行)")


# ============================================================
# 主流程
# ============================================================

def main():
    # ---- 输入 JSON 路径 ----
    input_path_str = input("请输入 output.json 的路径: ").strip()
    input_path = Path(input_path_str)

    if not input_path.exists():
        print(f"[错误] 文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 输出目录与输入 JSON 同目录
    out_dir = input_path.parent
    data_csv = str(out_dir / "data.csv")
    agg_csv = str(out_dir / "aggregation.csv")

    records = data.get("data", [])
    aggregations = data.get("aggregations", {})

    has_data = bool(records)
    has_agg = bool(aggregations)

    # ---- 情况1: 都为空 ----
    if not has_data and not has_agg:
        total = data.get("total", 0)
        count = data.get("count", 0)
        print(f"[提示] 数据记录和聚合统计均为空。total={total}, count={count}，未生成 CSV。")
        return

    # ---- 情况2: 只有聚合 ----
    if not has_data and has_agg:
        print("[提示] 数据记录为空，仅输出聚合统计 CSV。")
        agg_fieldnames, agg_rows = flatten_aggregations(aggregations)
        if agg_rows:
            write_csv(agg_csv, agg_fieldnames, agg_rows)
        else:
            print("[提示] 聚合统计解析后为空，未生成 CSV。")
        return

    # ---- 情况3: 只有数据记录 ----
    if has_data and not has_agg:
        print("[提示] 聚合统计为空，仅输出数据记录 CSV。")
        rows = []
        for idx, rec in enumerate(records, start=1):
            row = {"序号": idx}
            for field in DATA_FIELDS:
                row[field] = rec.get(field, "")
            rows.append(row)
        write_csv(data_csv, ["序号"] + DATA_FIELDS, rows)
        return

    # ---- 情况4: 两者都有 ----
    # 数据记录 CSV
    rows_data = []
    for idx, rec in enumerate(records, start=1):
        row = {"序号": idx}
        for field in DATA_FIELDS:
            row[field] = rec.get(field, "")
        rows_data.append(row)
    write_csv(data_csv, ["序号"] + DATA_FIELDS, rows_data)

    # 聚合统计 CSV
    agg_fieldnames, agg_rows = flatten_aggregations(aggregations)
    if agg_rows:
        write_csv(agg_csv, agg_fieldnames, agg_rows)
    else:
        print("[提示] 聚合统计解析后为空，未生成聚合 CSV。")

    print("[完成] 解析完毕。")


if __name__ == "__main__":
    main()
