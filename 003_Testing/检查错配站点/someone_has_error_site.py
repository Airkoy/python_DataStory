import argparse
import csv
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJoZXJtZXNfYWRtaW5AZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc4NTg5OTEwOTI2OSwicHciOiJoU204VzJNbXVIeT9KQCFOek0yVCIsImV4cCI6MTc4NjUwMzkwOX0.-RbcgqMZB5hMb_ljWAujmJVEBuQsNx4c1xTzzPhcClSrFZ19ZfuwfOgPu7LUZgYT_PYMbBcyk04epa4IRTSLLw"
}

BASE_URL = "https://dc.datastory.com.cn/admin/user/permission/detail"
MAX_WORKERS = 20
REQUEST_TIMEOUT = 15
MAX_ATTEMPTS = 2

PROJECT_ROOT = Path(__file__).resolve().parents[2]
USER_LIST_PATH = PROJECT_ROOT / "002_ds_koy_tools/charge_tools/user_list.json"
TARGET_NAMES_PATH = Path(__file__).resolve().parent / "target_names.json"
OUTPUT_PATH = Path(__file__).resolve().parent / "target_uid_results.csv"

thread_local = threading.local()


def get_session():
    """Each worker uses its own persistent HTTP session."""
    if not hasattr(thread_local, "session"):
        session = requests.Session()
        session.headers.update(headers)
        thread_local.session = session
    return thread_local.session


def load_target_names():
    with TARGET_NAMES_PATH.open(encoding="utf-8") as target_file:
        raw_target_names = json.load(target_file)

    if not isinstance(raw_target_names, list):
        raise ValueError("target_names.json must contain a JSON array")

    target_names = []
    seen = set()
    for index, value in enumerate(raw_target_names, start=1):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"target_names.json item {index} must be a non-empty string"
            )
        target_name = value.strip()
        if target_name not in seen:
            seen.add(target_name)
            target_names.append(target_name)

    if not target_names:
        raise ValueError("target_names.json must contain at least one target name")
    return target_names


def check_uid(account, uid, target_names):
    params = {"uid": uid, "uuu": "banyan"}
    last_error = ""

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = get_session().get(
                BASE_URL,
                params=params,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()

            if not payload.get("success"):
                raise RuntimeError(
                    f"API code={payload.get('code')} message={payload.get('message')}"
                )

            # Crawl application permissions are stored in applicationList.
            applications = (payload.get("data") or {}).get("applicationList") or []
            applications_by_name = {
                item.get("name"): item for item in applications if item.get("name")
            }
            matches = [
                {
                    "target_name": target_name,
                    "target_id": applications_by_name[target_name].get("id", ""),
                }
                for target_name in target_names
                if target_name in applications_by_name
            ]
            return {
                "account": account,
                "uid": uid,
                "matches": matches,
                "error": "",
            }
        except (requests.RequestException, ValueError, RuntimeError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt + 1 < MAX_ATTEMPTS:
                time.sleep(0.25)

    return {
        "account": account,
        "uid": uid,
        "matches": [],
        "error": last_error,
    }


def save_results(results):
    fieldnames = [
        "account",
        "uid",
        "target_name",
        "target_id",
        "error",
    ]
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            if result["error"]:
                writer.writerow(
                    {
                        "account": result["account"],
                        "uid": result["uid"],
                        "target_name": "",
                        "target_id": "",
                        "error": result["error"],
                    }
                )
            for match in result["matches"]:
                writer.writerow(
                    {
                        "account": result["account"],
                        "uid": result["uid"],
                        "target_name": match["target_name"],
                        "target_id": match["target_id"],
                        "error": "",
                    }
                )


def load_user_map(user_list_path):
    with user_list_path.open(encoding="utf-8") as user_file:
        users = json.load(user_file)
    if not isinstance(users, dict):
        raise ValueError(
            f"用户列表必须是 email 到 uid 的 JSON 对象: {user_list_path}"
        )

    metadata_path = user_list_path.with_suffix(".meta.json")
    if metadata_path.exists():
        with metadata_path.open(encoding="utf-8") as metadata_file:
            metadata = json.load(metadata_file)
        generated_at = metadata.get("generated_at", "未知")
    else:
        generated_at = "未记录"
    print(
        f"user_cache={user_list_path} generated_at={generated_at} "
        f"users={len(users)}"
    )
    return users


def main(user_list_path=USER_LIST_PATH):
    users = load_user_map(user_list_path)
    target_names = load_target_names()

    results = []
    total = len(users)
    started_at = time.monotonic()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(check_uid, account, uid, target_names): (account, uid)
            for account, uid in users.items()
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            results.append(future.result())
            if completed % 500 == 0 or completed == total:
                matched = sum(len(item["matches"]) for item in results)
                errors = sum(bool(item["error"]) for item in results)
                print(
                    f"progress={completed}/{total} "
                    f"matches={matched} errors={errors}",
                    flush=True,
                )

    results.sort(key=lambda item: item["uid"])
    save_results(results)

    matches = [
        {
            "account": result["account"],
            "uid": result["uid"],
            **match,
        }
        for result in results
        for match in result["matches"]
    ]
    errors = [item for item in results if item["error"]]
    counts_by_target = {target_name: 0 for target_name in target_names}
    for match in matches:
        counts_by_target[match["target_name"]] += 1

    print(f"checked={len(results)}")
    print(f"targets={len(target_names)}")
    print(f"matched_account_targets={len(matches)}")
    print(f"errors={len(errors)}")
    print(f"elapsed_seconds={time.monotonic() - started_at:.1f}")
    print(f"output={OUTPUT_PATH}")
    print("counts_by_target:")
    for target_name, count in counts_by_target.items():
        print(f"{target_name}: {count}")
    print("matches:")
    for match in matches:
        print(
            f"target={match['target_name']} "
            f"uid={match['uid']} account={match['account']}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="检查用户的站点权限错配")
    parser.add_argument(
        "--user-list",
        type=Path,
        default=USER_LIST_PATH,
        help=f"用户缓存文件（默认: {USER_LIST_PATH}）",
    )
    args = parser.parse_args()
    main(args.user_list)
