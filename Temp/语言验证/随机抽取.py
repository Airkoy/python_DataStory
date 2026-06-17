import pandas as pd
import glob
import os

# ================= 配置区域 =================
# 方式一：指定文件夹路径，程序会自动读取该文件夹下所有的 .xlsx 文件
input_folder = r'D:\python_project\python_DataStory\Temp\语言验证\抽样文件'

# 方式二：手动指定多个文件路径列表（如果你只想处理特定的几个文件，注释掉方式一，用方式二）
# input_files = ['文件1.xlsx', '文件2.xlsx', '文件3.xlsx']

output_file = '随机抽取结果1.xlsx'  # 导出的新 Excel 文件名
columns_to_extract = ["id", "站点名称", "标题","内容","url","语言"]  # 需要提取的列名
sample_size = 10000  # 随机抽取的行数
# ============================================

# 获取需要处理的文件列表
if 'input_folder' in locals() and input_folder:
    # 查找文件夹下所有的 xlsx 文件
    file_list = glob.glob(os.path.join(input_folder, '*.xlsx'))
else:
    file_list = None

if not file_list:
    print("❌ 错误：未找到任何 Excel 文件，请检查路径配置。")
else:
    print(f"找到 {len(file_list)} 个文件待处理：{file_list}")

    all_data = []  # 用于存储从每个文件中提取的数据

    for file_path in file_list:
        try:
            print(f"正在读取: {os.path.basename(file_path)} ...")
            df = pd.read_excel(file_path)

            # 提取指定列。如果原文件缺失某列，reindex会自动填充为 NaN，防止报错
            df_selected = df.reindex(columns=columns_to_extract)

            # 将非空数据加入列表（如果某行这三列全为空则丢弃）
            all_data.append(df_selected.dropna(how='all'))

        except Exception as e:
            print(f"  ⚠️ 读取 {os.path.basename(file_path)} 失败，已跳过。错误: {e}")

    if not all_data:
        print("❌ 错误：未能从任何文件中读取到有效数据。")
    else:
        # 1. 将所有文件的数据纵向拼接到一起
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"\n数据合并完成，总计获取 {len(combined_df)} 行有效数据。")

        # 2. 随机抽取 1000 行
        # n: 抽取数量； random_state: 随机种子（不填则每次运行结果不同，填了则结果固定可复现）
        # 如果总数据量不足 1000 行，则取全部数据 n=len(combined_df)
        actual_sample_size = min(sample_size, len(combined_df))

        sampled_df = combined_df.sample(n=actual_sample_size, random_state=None)

        # 3. 导出到新的 Excel
        sampled_df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"✅ 处理完成！已随机抽取 {len(sampled_df)} 行数据并导出到: {output_file}")