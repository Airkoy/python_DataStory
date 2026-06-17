import pandas as pd
import json


def extract_mapping_with_sample(csv_file_path, output_excel_path):
    print(f"正在读取文件: {csv_file_path} ...")
    df = pd.read_csv(csv_file_path)

    # 用于存储最终结果
    result_data = []
    # 用于记录已经处理过的组合，确保示例数据只取第一条
    seen_combinations = set()

    for index, row in df.iterrows():
        output_type = row.get('output')
        app_id = row.get('app_id')
        update_time = row.get('last_update_time')
        json_str = row.get('json')

        # 如果核心字段为空，跳过该行
        if pd.isna(output_type) or pd.isna(app_id) or pd.isna(json_str):
            continue

        try:
            # 解析 json 列
            json_data = json.loads(json_str)
            # 兼容 json 数据是列表或单条字典的情况
            records = json_data if isinstance(json_data, list) else [json_data]

            for record in records:
                if isinstance(record, dict):
                    s_id = str(record.get('站点id', ''))
                    s_name = str(record.get('站点名称', ''))

                    # 如果没有站点信息则跳过
                    if not s_id or not s_name:
                        continue

                    # 构建唯一标识组合
                    combo_key = (output_type, app_id, update_time, s_id, s_name)

                    # 如果这个组合已经处理过，则跳过（保证示例数据只取第一条）
                    if combo_key in seen_combinations:
                        continue

                    # 标记该组合已处理
                    seen_combinations.add(combo_key)

                    # 将该条 record 原样转回 JSON 字符串，作为示例数据
                    # ensure_ascii=False 可以保留中文，indent=None 压缩成一行方便在 Excel 中查看
                    sample_json_str = json.dumps(record, ensure_ascii=False)

                    result_data.append({
                        'output': output_type,
                        'app_id': app_id,
                        '站点id': s_id,
                        '站点名称': s_name,
                        '示例数据': sample_json_str,
                        '最后更新时间': update_time
                    })

        except json.JSONDecodeError:
            print(f"警告：第 {index + 1} 行的 json 数据解析失败")

    # 创建 DataFrame
    df_result = pd.DataFrame(result_data)

    if not df_result.empty:
        # 额外去重保障
        df_result = df_result.drop_duplicates().reset_index(drop=True)

    # 保存为 Excel 文件
    df_result.to_excel(output_excel_path, index=False, engine='openpyxl')
    print(f"提取完成！共找到 {len(df_result)} 条唯一映射关系。")
    print(f"结果已保存至: {output_excel_path}")


# 使用示例
if __name__ == "__main__":
    # 替换为您的实际 CSV 文件路径
    input_csv = "db_datastory_hermes_rmes_application_demo.csv"

    # 输出的 Excel 文件名
    output_excel = "output_app_site_sample.xlsx"

    extract_mapping_with_sample(input_csv, output_excel)