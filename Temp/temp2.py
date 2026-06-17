import pandas as pd
import numpy as np
import json


def process_excel_file(file_path):
    print(f"正在读取文件: {file_path} ...")

    try:
        # 1. 读取 Excel 文件，强制使用 calamine 引擎（解决 openpyxl 样式报错问题，且速度极快）
        df = pd.read_excel(file_path, sheet_name='特定站点', header=None, engine='calamine')
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 '{file_path}'，请检查路径。")
        return
    except Exception as e:
        print(f"❌ 读取文件时发生错误: {e}")
        return

    # 2. 去掉前两行表头说明
    df = df.iloc[2:].reset_index(drop=True)

    # 3. 按列索引提取数据
    col_site_name = df[2]
    col_app_id = df[3]
    col_scope_id = df[4]
    col_site_id = df[8]
    col_cat_id = df[10]

    # 4. 数据清洗与填充逻辑
    # calamine 引擎读出来的空单元格通常是 None，我们把 '*' 也统一替换掉
    replace_val = {'*': np.nan, '': np.nan}

    col_site_name = col_site_name.replace(replace_val)
    col_app_id = col_app_id.replace(replace_val)
    col_scope_id = col_scope_id.replace(replace_val)
    col_site_id = col_site_id.replace(replace_val)
    col_cat_id = col_cat_id.replace(replace_val)

    # 站点名称、app_id、scope_id 属于合并单元格属性，向下填充
    col_site_name = col_site_name.ffill()
    col_app_id = col_app_id.ffill()
    col_scope_id = col_scope_id.ffill()

    # 5. 组装新的 DataFrame
    result_df = pd.DataFrame({
        '站点名称': col_site_name,
        'site_id': col_site_id,
        'cat_id': col_cat_id,
        'app_id': col_app_id,
        'scope_id': col_scope_id
    })

    # 过滤掉 site_id 和 cat_id 都为空的行（去除纯配置参数行）
    result_df = result_df.dropna(subset=['site_id', 'cat_id'], how='all')

    # 6. 数据类型转换 (处理 101993.0 转整数，处理特殊字符保留字符串)
    def safe_convert(val):
        if pd.isna(val):
            return None
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return str(val)

    for col in ['site_id', 'cat_id', 'app_id', 'scope_id']:
        result_df[col] = result_df[col].apply(safe_convert)

    result_df['站点名称'] = result_df['站点名称'].where(pd.notna(result_df['站点名称']), None)

    # 7. 导出为 JSON 文件
    json_filename = 'sites_info.json'
    json_data = result_df.to_dict(orient='records')
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    print(f"✅ 成功导出 JSON 文件: {json_filename}")

    # 8. 导出为 Excel 文件 (导出时依然用默认引擎即可，导出的文件是干净的)
    excel_filename = 'sites_info.xlsx'
    result_df.to_excel(excel_filename, index=False)
    print(f"✅ 成功导出 Excel 文件: {excel_filename}")


# ==========================================
# 运行入口
# ==========================================
if __name__ == '__main__':
    # 绝对路径
    input_file = r'C:\Users\Airkoy\Desktop\聚合-数据超市站点区域信息.xlsx'

    process_excel_file(input_file)
