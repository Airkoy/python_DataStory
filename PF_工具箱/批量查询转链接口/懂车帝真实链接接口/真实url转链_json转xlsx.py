import pandas as pd

# 读取结果文件（注意：虽然叫 .json，但实际是文本行格式）
input_file = 'converted_result.json'
output_file = '194条的转链结果.xlsx'

rows = []

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if '|' in line:
            original, converted = line.split('|', 1)  # 只分割第一个 |
            rows.append({'Original URL': original, 'Converted URL': converted})
        else:
            rows.append({'Original URL': line, 'Converted URL': ''})

# 创建 DataFrame
df = pd.DataFrame(rows)

# 写入 Excel
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"✅ 已成功写入 Excel 文件：{output_file}")
print(f"📊 共处理 {len(df)} 行数据")