import pandas as pd
import os


# 用法：在最下面的folder输入文件夹名称，就可以把文件夹内所有的xlsx文件合并成一个

def simple_merge_excel(folder_path, output_name="merged_files.xlsx"):
    """简化版的xlsx文件合并函数"""

    # 获取所有xlsx文件
    excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

    if not excel_files:
        print("没有找到xlsx文件")
        return

    # 合并文件
    all_data = []
    for file in excel_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_excel(file_path)
        df['来源文件'] = file  # 添加来源文件列
        all_data.append(df)
        print(f"已添加: {file}")

    # 保存合并结果
    merged_df = pd.concat(all_data, ignore_index=True)
    output_path = os.path.join(folder_path, output_name)
    merged_df.to_excel(output_path, index=False)

    print(f"\n合并完成！共合并 {len(excel_files)} 个文件")
    print(f"总数据行数: {len(merged_df)}")
    print(f"保存位置: {output_path}")


# 使用示例
folder = r"C:\Users\Airkoy\Desktop\知乎_zvideo"
# folder = r"C:\Users\Airkoy\Desktop\知乎_articles"
# folder = r"C:\Users\Airkoy\Desktop\知乎_questions"
# folder = r"C:\Users\Airkoy\Desktop\知乎_pins"

simple_merge_excel(folder)
