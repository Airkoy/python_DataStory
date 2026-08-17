import requests
import json
import pandas as pd
import os
import sys
from datetime import datetime


url = 'https://dc.datastory.com.cn/auth/obtain'
# url = 'http://dc.dev.datastory.com.cn/auth/obtain'

# 管理员账号
data = {
    "username": "hermes_admin@datastory.com.cn",
    "password": "hSm8W2MmuHy?J@!NzM2T"
    # "password": "123456", # 测试环境
}

response = requests.post(url, data=data)

# 直接提取token并构建headers
token = response.json()['data']
headers = {
    "Content-Type": 'application/json',
    'Authorization': token,
}

SEARCH_URL = "https://dc.datastory.com.cn/monitor/account/wechatVideo/batchSearch?uuu=banyan"
ADD_URL = "https://dc.datastory.com.cn/monitor/account/wechatVideo/add?uuu=banyan"


def load_names_from_file(filepath):
    """从文件中读取视频号名称列表。

    支持三种输入格式：
    1. JSON数组：["名称1", "名称2"]
    2. JSONL格式：每行一个JSON字符串 或 {"name": "名称"}
    3. 纯文本格式：每行一个名称
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # 格式1：尝试解析为JSON数组
    if content.startswith('['):
        try:
            names = json.loads(content)
            if isinstance(names, list):
                return _dedupe([str(n).strip() for n in names if n and str(n).strip()])
        except json.JSONDecodeError:
            pass

    # 格式2/3：按行读取
    names = []
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        # 尝试解析为JSON（可能是JSONL中的字符串或对象）
        try:
            parsed = json.loads(line)
            if isinstance(parsed, str):
                names.append(parsed.strip())
            elif isinstance(parsed, dict):
                name = parsed.get('name') or parsed.get('nickName') or parsed.get('名称') or str(parsed)
                names.append(str(name).strip())
            else:
                names.append(str(parsed).strip())
        except json.JSONDecodeError:
            # 纯文本行
            names.append(line)

    return _dedupe(names)


def _dedupe(items):
    """去重并保持插入顺序"""
    seen = set()
    result = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def search_uid(name):
    """查询单个视频号的UID"""
    data = {"name": [name]}
    try:
        resp = requests.post(SEARCH_URL, headers=headers, data=json.dumps(data), timeout=15)
        result = resp.json()
        uids = result.get("data", {}).get("uids", [])
        if uids:
            return uids[0].get("uid", "")
        return ""
    except Exception as e:
        print(f"  [ERROR] {name}: {e}", flush=True)
        return ""


def add_monitor(name, uid):
    """添加单个视频号监控"""
    payload = json.dumps({"accounts": [{"name": name, "uid": uid}]}, ensure_ascii=False)
    try:
        resp = requests.post(ADD_URL, headers=headers, data=payload, timeout=30)
        return resp.text
    except Exception as e:
        return f"ERROR: {e}"


def main():
    # ---- 输入文件 ----
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, "wechatVideo_list.json")

    if not os.path.exists(input_file):
        print(f"输入文件不存在: {input_file}")
        print("用法: python batch_urlQuery_urlMonitor.py <输入文件路径>")
        sys.exit(1)

    output_dir = 'result'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    xlsx_output = os.path.join(output_dir, f"视频号UID_{timestamp}.xlsx")
    csv_output = os.path.join(output_dir, f"视频号添加监控结果_{timestamp}.csv")

    # ========== 步骤1：读取名称 ==========
    names = load_names_from_file(input_file)
    if not names:
        print("未读取到任何有效名称，请检查输入文件格式。")
        sys.exit(1)
    print(f"共读取到 {len(names)} 个视频号名称（已去重）\n")

    # ========== 步骤2：逐个查询UID ==========
    print("=" * 50)
    print("开始查询UID...")
    print("=" * 50)

    name_uid_map = {}
    for i, name in enumerate(names, 1):
        uid = search_uid(name)
        name_uid_map[name] = uid
        tag = "OK" if uid else "NOT_FOUND"
        print(f"  [{i}/{len(names)}] {tag} {name}" + (f" -> {uid}" if uid else ""))

    found = sum(1 for v in name_uid_map.values() if v)
    print(f"\nUID查询完成: {found}/{len(names)} 个账号找到UID\n")

    # ========== 步骤3：保存XLSX ==========
    df_uid = pd.DataFrame([
        {"微信视频号名称": name, "uid": uid}
        for name, uid in name_uid_map.items()
    ])
    df_uid.to_excel(xlsx_output, index=False, sheet_name="UID查询结果")
    print(f"XLSX已保存: {xlsx_output}")

    # ========== 步骤4：逐个添加监控 + 收集结果 ==========
    print("\n" + "=" * 50)
    print("开始添加监控...")
    print("=" * 50)

    accounts_with_uid = [(n, u) for n, u in name_uid_map.items() if u]
    monitor_records = []

    for i, (name, uid) in enumerate(accounts_with_uid, 1):
        result_text = add_monitor(name, uid)
        is_success = '"success":true' in result_text or '"code":0' in result_text or '"code": 0' in result_text
        tag = "SUCCESS" if is_success else "FAIL"
        print(f"  [{i}/{len(accounts_with_uid)}] {tag} {name} | {result_text[:120]}")
        monitor_records.append({
            "名称": name,
            "uid": uid,
            "添加监控结果": result_text
        })

    # 无UID的账号也记录
    for name, uid in name_uid_map.items():
        if not uid:
            monitor_records.append({
                "名称": name,
                "uid": "",
                "添加监控结果": "未找到UID，无法添加监控"
            })

    # ========== 步骤5：保存CSV ==========
    df_monitor = pd.DataFrame(monitor_records)
    df_monitor.to_csv(csv_output, index=False, encoding='utf-8-sig')
    print(f"\nCSV已保存: {csv_output}")

    # ========== 统计输出 ==========
    success = sum(1 for r in monitor_records
                  if '"success":true' in r["添加监控结果"] or '"code":0' in r["添加监控结果"] or '"code": 0' in r["添加监控结果"])
    print("\n" + "=" * 50)
    print("全部完成！")
    print(f"   总名称数:      {len(names)}")
    print(f"   找到UID:       {found}")
    print(f"   添加监控成功:  {success}")
    print(f"   XLSX输出:      {xlsx_output}")
    print(f"   CSV输出:       {csv_output}")
    print("=" * 50)


if __name__ == "__main__":
    main()
