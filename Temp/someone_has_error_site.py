import os
import csv
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

headers = {
    "Content-Type": "application/json",
    "Authorization": os.environ["DATASTORY_AUTHORIZATION"]
}

BASE_URL = "https://dc.datastory.com.cn/admin/user/permission/detail"
TARGET_NAME = "elotrolado"
MAX_WORKERS = 20
REQUEST_TIMEOUT = 15
MAX_ATTEMPTS = 2

PROJECT_ROOT = Path(__file__).resolve().parents[1]
USER_LIST_PATH = PROJECT_ROOT / "ds_koy_tools/charge_tools/user_list.json"
OUTPUT_FILE_NAME = "".join(
    char if char.isalnum() or char in "-_." else "_" for char in TARGET_NAME
)
OUTPUT_PATH = Path(__file__).resolve().parent / f"{OUTPUT_FILE_NAME}_uid_results.csv"

thread_local = threading.local()


def get_session():
    """Each worker uses its own persistent HTTP session."""
    if not hasattr(thread_local, "session"):
        session = requests.Session()
        session.headers.update(headers)
        thread_local.session = session
    return thread_local.session


def check_uid(account, uid):
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
            target = next(
                (item for item in applications if item.get("name") == TARGET_NAME),
                None,
            )
            return {
                "account": account,
                "uid": uid,
                "target_name": TARGET_NAME,
                "contains_target": target is not None,
                "target_id": (target or {}).get("id", ""),
                "error": "",
            }
        except (requests.RequestException, ValueError, RuntimeError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt + 1 < MAX_ATTEMPTS:
                time.sleep(0.25)

    return {
        "account": account,
        "uid": uid,
        "target_name": TARGET_NAME,
        "contains_target": False,
        "target_id": "",
        "error": last_error,
    }


def save_results(results):
    fieldnames = [
        "account",
        "uid",
        "target_name",
        "contains_target",
        "target_id",
        "error",
    ]
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def main():
    with USER_LIST_PATH.open(encoding="utf-8") as user_file:
        users = json.load(user_file)

    results = []
    total = len(users)
    started_at = time.monotonic()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(check_uid, account, uid): (account, uid)
            for account, uid in users.items()
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            results.append(future.result())
            if completed % 500 == 0 or completed == total:
                matched = sum(item["contains_target"] for item in results)
                errors = sum(bool(item["error"]) for item in results)
                print(
                    f"progress={completed}/{total} "
                    f"matches={matched} errors={errors}",
                    flush=True,
                )

    results.sort(key=lambda item: item["uid"])
    save_results(results)

    matches = [item for item in results if item["contains_target"]]
    errors = [item for item in results if item["error"]]

    print(f"checked={len(results)}")
    print(f"target={TARGET_NAME}")
    print(f"matched={len(matches)}")
    print(f"errors={len(errors)}")
    print(f"elapsed_seconds={time.monotonic() - started_at:.1f}")
    print(f"output={OUTPUT_PATH}")
    print("matches:")
    for item in matches:
        print(f"uid={item['uid']} account={item['account']}")


if __name__ == "__main__":
    main()
