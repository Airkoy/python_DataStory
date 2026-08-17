import json
import csv
import argparse
import os
from elasticsearch import Elasticsearch

ES_CONFIG = {
    "hosts": ["https://es-banyan-global.datastory.com.cn"],
    "basic_auth": ("banyan-custom", "banyan-custom-zxcv"),
    "request_timeout": 60,
}

INDEX_ALIAS = {
    "tiktok": "ds-banyan-tiktok-post-index-v3",
    "globalmedia": "ds-banyan-globalmedia-post-index-v3",
    "globalnewsforum": "ds-banyan-globalnewsforum-post-index-v3",
    "twitter": "ds-banyan-twitter-post-index-v3",
}


def query_to_csv(
    index,
    query_body,
    source_fields,
    output_dir=".",
    scroll_size=1000,
    max_hits=None,
    output_prefix="export",
):
    """
    Execute ES query using scroll API, extract URLs grouped by target fields.

    For each non-url field in source_fields (e.g. "has_partner_brand", "sponsor_names"),
    generates a CSV containing URLs from hits where that field exists and is non-empty.

    Parameters
    ----------
    index : str
        ES index name, or alias key in INDEX_ALIAS.
    query_body : dict
        ES query body (the "query" part).
    source_fields : list[str]
        Fields to include in _source. Must include "url".
    output_dir : str
        Directory for output CSV files.
    scroll_size : int
        Batch size per scroll request.
    max_hits : int or None
        Limit total hits (None = no limit, fetches all).
    output_prefix : str
        Prefix for output CSV filenames.
    """
    if index in INDEX_ALIAS:
        index = INDEX_ALIAS[index]

    es = Elasticsearch(**ES_CONFIG)

    body = {"query": query_body, "_source": source_fields}

    all_hits = []
    resp = es.search(
        index=index,
        body=body,
        size=scroll_size,
        scroll="5m",
    )
    scroll_id = resp["_scroll_id"]
    hits = resp["hits"]["hits"]
    all_hits.extend(hits)
    total = resp["hits"]["total"]["value"]
    print(f"Total hits: {total}, fetched: {len(all_hits)}")

    while len(hits) > 0:
        resp = es.scroll(scroll_id=scroll_id, scroll="5m")
        scroll_id = resp["_scroll_id"]
        hits = resp["hits"]["hits"]
        all_hits.extend(hits)
        if max_hits and len(all_hits) >= max_hits:
            all_hits = all_hits[:max_hits]
            break
        if len(all_hits) % (scroll_size * 5) == 0:
            print(f"  progress: {len(all_hits)}/{total}")

    es.clear_scroll(scroll_id=scroll_id)
    print(f"Done scrolling, {len(all_hits)} hits collected.")

    os.makedirs(output_dir, exist_ok=True)

    export_fields = [f for f in source_fields if f != "url"]
    if not export_fields:
        urls = [h["_source"].get("url") for h in all_hits]
        urls = [u for u in urls if u]
        filename = os.path.join(output_dir, f"{output_prefix}_url.csv")
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["url"])
            for url in urls:
                writer.writerow([url])
        print(f"Exported {len(urls)} URLs -> {filename}")
        return

    for field in export_fields:
        urls = [
            h["_source"]["url"]
            for h in all_hits
            if field in h.get("_source", {})
            and h["_source"].get(field)
            and h["_source"].get("url")
        ]
        filename = os.path.join(output_dir, f"{output_prefix}_{field}.csv")
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["url"])
            for url in urls:
                writer.writerow([url])
        print(f"Exported {len(urls)} URLs -> {filename}")


def run_from_config(config_path):
    """
    Read a JSON config file and run query_to_csv.

    Config format:
    {
      "index": "ds-banyan-globalmedia-post-index-v3",  // or alias "globalmedia"
      "_source": ["url", "has_partner_brand", "sponsor_names"],
      "query": { ... },
      "output_prefix": "ins",
      "output_dir": ".",
      "scroll_size": 1000,
      "max_hits": 10000
    }
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    query_to_csv(
        index=config["index"],
        query_body=config["query"],
        source_fields=config.get("_source", ["url"]),
        output_dir=config.get("output_dir", "."),
        scroll_size=config.get("scroll_size", 1000),
        max_hits=config.get("max_hits"),
        output_prefix=config.get("output_prefix", "export"),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Query ES and export URL CSVs grouped by source fields."
    )
    parser.add_argument(
        "config", nargs="?", default="query_config_sample.json",
        help="Path to JSON config file (default: query_config.json)"
    )
    args = parser.parse_args()
    run_from_config(args.config)

