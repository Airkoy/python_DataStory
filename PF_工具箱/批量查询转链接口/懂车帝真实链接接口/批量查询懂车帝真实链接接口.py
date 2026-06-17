import requests
import json

# 读取原始URL列表（每行一个）
with open('text.json', 'r', encoding='utf-8') as f:
    raw_urls = [line.strip() for line in f if line.strip()]

output_lines = []

for url in raw_urls:
    payload = json.dumps({"urls": url})
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(
            "http://api.rhino.datastory.com.cn/dongchedi/UrlConvert",
            headers=headers,
            data=payload,
            timeout=10
        )
        result = response.json()

        if result.get("code") == 0 and result.get("data") and result["data"].get("success"):
            converted_url = result["data"]["success"][0]
            output_lines.append(f"{url}|{converted_url}")
            print(f"✅ {url} -> {converted_url}")
        else:
            # 转换失败，只保留原URL
            output_lines.append(url)
            print(f"❌ 转换失败: {url}")

    except Exception as e:
        # 请求异常，也视为失败
        output_lines.append(url)
        print(f"⚠️ 请求异常 ({url}): {e}")

# 写入结果文件（每行一个，非标准JSON，但按你要求命名为.json）
with open('converted_result.json', 'w', encoding='utf-8') as f:
    for line in output_lines:
        f.write(line + '\n')

print(f"\n🎉 处理完成！共 {len(output_lines)} 行，结果已保存至 converted_result.json")
