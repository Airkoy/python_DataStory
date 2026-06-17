import pandas as pd
import requests
import json
import time
import os

# ================= 配置区域 =================
API_URL = "http://api.rhino.datastory.com.cn/rs/common/urlConvertHandler"
HEADERS = {'Content-Type': 'application/json'}
INPUT_FILE = "url.json"

# 输出文件名
OUTPUT_EXCEL = "转链结果查询结果/转链对照结果.xlsx"
OUTPUT_TXT = "转链结果查询结果/转链结果.txt"
OUTPUT_JSON = "转链结果查询结果/全量库查询.json"


# ===========================================

def main():
    # 确保输出目录存在
    for out_file in (OUTPUT_EXCEL, OUTPUT_TXT, OUTPUT_JSON):
        out_dir = os.path.dirname(out_file)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

    # 读取原始 JSON 文件
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()

            # 兼容处理：尝试按标准JSON解析，如果失败则按换行符分割纯文本
            try:
                url_list = json.loads(content)
                if not isinstance(url_list, list):
                    url_list = [str(url_list)]
            except json.JSONDecodeError:
                # 如果不是标准JSON格式，按行分割
                url_list = [line.strip() for line in content.split('\n') if line.strip()]

    except FileNotFoundError:
        print(f"错误：找不到文件 {INPUT_FILE}")
        return
    except Exception as e:
        print(f"读取文件失败: {e}")
        return

    # 存储用于生成 Excel 的记录 (包含成功和失败)
    excel_records = []

    # 存储用于生成 TXT 和 JSON 的成功 UID 列表
    success_uid_list = []

    # 统计计数
    total_count = 0
    success_count = 0
    fail_count = 0

    print(f"共读取到 {len(url_list)} 个 URL，开始处理转换...")

    for original_url in url_list:
        total_count += 1

        # 跳过空URL
        if not original_url:
            continue

        record = {"原始url": str(original_url)}  # 初始化记录
        is_success = False

        try:
            # 构造 payload
            payload = json.dumps({"urls": str(original_url)})
            response = requests.post(API_URL, headers=HEADERS, data=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()
                data = result.get("data", {})
                trans_error = data.get("transError", [])
                trans_uid_list = data.get("itemId", [])

                # 检查是否失败
                # 逻辑：如果在 transError 中 或者 返回的 itemId 为空，视为失败
                if str(original_url) in trans_error or not trans_uid_list:
                    fail_count += 1
                    record["状态"] = "失败"
                    record["转链后uid"] = ""
                    print(f"[失败] {original_url}")
                else:
                    # 成功情况
                    is_success = True
                    success_count += 1
                    uid_str = trans_uid_list[0]  # 提取 UID

                    record["状态"] = "成功"
                    record["转链后uid"] = uid_str

                    # 加入成功列表，用于后续生成 TXT 和 JSON
                    success_uid_list.append(uid_str)
                    print(f"[成功] {original_url} -> {uid_str}")
            else:
                # HTTP 错误
                fail_count += 1
                record["状态"] = "失败"
                record["转链后uid"] = ""
                print(f"[请求失败] {original_url} - HTTP {response.status_code}")

        except Exception as e:
            # 异常捕获
            fail_count += 1
            record["状态"] = "失败"
            record["转链后uid"] = ""
            print(f"[异常] {original_url} - {e}")

        # 将记录加入总列表
        excel_records.append(record)

        # 延迟，避免触发限流
        time.sleep(0.2)

    # ================= 生成文件 1: Excel =================
    if excel_records:
        df_result = pd.DataFrame(excel_records)
        # 调整列顺序
        cols_to_keep = ["原始url", "转链后uid", "状态"]
        # 确保列存在
        final_df = df_result[[c for c in cols_to_keep if c in df_result.columns]]

        final_df.to_excel(OUTPUT_EXCEL, index=False)
        print(f"\n[文件1已生成] {OUTPUT_EXCEL}")
        print(f"  - 总记录: {len(excel_records)} | 成功: {success_count} | 失败: {fail_count}")
    else:
        print("\n无数据可生成 Excel。")

    # ================= 生成文件 2: TXT =================
    # 格式: {"cnt":N,"uid":"id1,id2,..."}
    if success_uid_list:
        cnt = len(success_uid_list)
        uid_string = ",".join(success_uid_list)

        result_data = {
            "cnt": cnt,
            "uid": uid_string
        }

        json_str = json.dumps(result_data, separators=(',', ':'), ensure_ascii=False)

        with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
            f.write(json_str)

        print(f"[文件2已生成] {OUTPUT_TXT}")
    else:
        print(f"\n[文件2未生成] 没有成功的 UID。")

    # ================= 生成文件 3: JSON (全量库查询) =================

    if success_uid_list:
        json_data = {
            "fieldValue": success_uid_list  # 这是一个列表 ['@id1', '@id2']
        }

        # 使用 indent=2 让文件更易读，separators 去除多余空格
        json_content = json.dumps(json_data, ensure_ascii=False, indent=2)

        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            f.write(json_content)

        print(f"[文件3已生成] {OUTPUT_JSON}")
        print(f"  - 内容预览:\n{json_content}")
    else:
        print(f"\n[文件3未生成] 没有成功的 UID。")

    print("\n=== 所有任务完成 ===")


if __name__ == "__main__":
    main()