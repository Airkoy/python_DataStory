"""
测试环境 - 获取站点示例数据列表
GET http://dc.dev.datastory.com.cn/app/demo/getList?appId=6

功能：查询指定 appId 下的所有示例数据记录，提取 id/appId/output/lastUpdateTime
      并导出到 CSV 文件。
"""
import csv
import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests

# ---- 配置 ----
AUTH_URL = "http://dc.dev.datastory.com.cn/auth/obtain"
GET_LIST_URL = "http://dc.dev.datastory.com.cn/app/demo/getList"

# site_info JSON 文件路径（包含所有站点的 app_id）
SITE_INFO_JSON = Path(__file__).resolve().parent.parent.parent / "Elasticsearch查询" / "site_info_260625.json"

# 输出 CSV 文件路径（与本脚本同目录）
OUTPUT_CSV = Path(__file__).resolve().parent / "site_example_list.csv"

# 北京时间时区
TZ_BEIJING = timezone(timedelta(hours=8))


def load_app_ids(json_path: Path) -> list[str]:
    """从 site_info JSON 文件中提取所有去重后的非空 app_id。"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    app_ids = set()
    for item in data:
        aid = item.get("app_id", "")
        if aid:  # 过滤空字符串
            app_ids.add(aid)

    # 按数值排序，保持稳定顺序
    return sorted(app_ids, key=int)


def _timestamp_to_str(ts_millis: int) -> str:
    """将毫秒级 Unix 时间戳转为 yyyy:MM:dd-HH:mm:ss（北京时间）。"""
    dt = datetime.fromtimestamp(ts_millis / 1000.0, tz=TZ_BEIJING)
    return dt.strftime("%Y:%m:%d-%H:%M:%S")


def fetch_example_list(app_id: str) -> list[dict]:
    """调用接口获取指定 appId 的示例数据列表，返回 data 数组。"""
    # 1. 获取 Token
    login_data = {
        "username": "hermes_admin@datastory.com.cn",
        "password": "123456",  # 测试环境
    }
    resp = requests.post(AUTH_URL, data=login_data)
    resp.raise_for_status()
    token = resp.json()["data"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
    }

    # 2. 查询列表
    resp = requests.get(GET_LIST_URL, params={"appId": app_id}, headers=headers)
    resp.raise_for_status()
    result = resp.json()

    if not result.get("success"):
        raise RuntimeError(f"接口返回失败: {result.get('message', '未知错误')}")

    return result.get("data", [])


def _build_rows(records: list[dict]) -> list[list]:
    """将原始记录列表转换为 CSV 行列表（不含表头）。"""
    rows = []
    for item in records:
        ts = item.get("lastUpdateTime", 0)
        if isinstance(ts, (int, float)) and ts > 0:
            formatted = _timestamp_to_str(int(ts))
        else:
            formatted = ""
        rows.append([
            str(item.get("id", "")),
            str(item.get("appId", "")),
            item.get("output", ""),
            formatted,
        ])
    return rows


def _load_existing_keys(csv_path: Path) -> set[tuple]:
    """
    从已有 CSV 中读取已存在记录的 (id, appId, lastUpdateTime) 三元组集合。
    如果文件不存在则返回空集合。
    """
    if not csv_path.exists():
        return set()

    existing = set()
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # 跳过表头
        if header is None:
            return set()
        for row in reader:
            if len(row) >= 4:
                # 按 (id, appId, lastUpdateTime) 作为去重键
                existing.add((row[0].strip(), row[1].strip(), row[3].strip()))
    return existing


def export_to_csv(records: list[dict], csv_path: Path):
    """
    将记录以**追加**方式写入 CSV，同时按 id + appId + lastUpdateTime 去重。

    - 如果 CSV 文件不存在或为空，则先写入表头，再写入数据行。
    - 如果 CSV 文件已存在，读取已有记录，只追加不重复的新行。
    - 已存在且 id/appId/lastUpdateTime 全部相同的记录将被跳过。

    CSV 包含 id, appId, output, lastUpdateTime 四列。
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    all_rows = _build_rows(records)
    if not all_rows:
        print("没有新数据需要写入。")
        return

    # 加载已存在的记录键（id, appId, lastUpdateTime）
    existing_keys = _load_existing_keys(csv_path)

    # 过滤掉已存在的重复记录
    new_rows = []
    skipped = 0
    for row in all_rows:
        key = (row[0], row[1], row[3])
        if key in existing_keys:
            skipped += 1
        else:
            new_rows.append(row)
            existing_keys.add(key)  # 避免同批次内部重复

    if not new_rows:
        print(f"所有 {len(all_rows)} 条记录均已存在，跳过写入（去重 {skipped} 条）。")
        return

    # 判断是否需要写入表头：文件不存在 或 文件为空
    need_header = not csv_path.exists() or csv_path.stat().st_size == 0

    with open(csv_path, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if need_header:
            writer.writerow(["id", "appId", "output", "lastUpdateTime"])
        writer.writerows(new_rows)

    print(f"已追加 {len(new_rows)} 条记录到: {csv_path}" + (f"（跳过重复 {skipped} 条）" if skipped else ""))


# --- 主程序入口 ---
if __name__ == "__main__":
    try:
        # 1. 从 JSON 加载所有去重后的 app_id
        app_ids = load_app_ids(SITE_INFO_JSON)
        print(f"从 {SITE_INFO_JSON.name} 加载到 {len(app_ids)} 个去重 app_id：{app_ids}")

        # 2. 遍历每个 app_id 获取示例数据
        all_records: list[dict] = []
        for aid in app_ids:
            try:
                records = fetch_example_list(aid)
                print(f"  appId={aid}: 获取到 {len(records)} 条记录")
                all_records.extend(records)
            except Exception as e:
                print(f"  ⚠ appId={aid} 获取失败: {e}，跳过继续...")

        print(f"\n共获取到 {len(all_records)} 条示例数据记录：")
        for r in all_records:
            ts = r.get("lastUpdateTime", 0)
            formatted = _timestamp_to_str(int(ts)) if isinstance(ts, (int, float)) and ts > 0 else ""
            print(f"  id={r['id']}, appId={r['appId']}, output={r['output']}, lastUpdateTime={formatted}")

        export_to_csv(all_records, OUTPUT_CSV)

    except requests.exceptions.Timeout:
        print("\n❌ 请求超时")
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP 错误: {e}")
        if e.response is not None:
            print(f"响应内容: {e.response.text[:500]}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 网络请求异常: {e}")
    except Exception as e:
        print(f"\n❌ 发生未知错误: {e}")
