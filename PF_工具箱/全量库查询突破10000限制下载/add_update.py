import pandas as pd
import os
import warnings


def safe_merge_excel(folder_path, output_name="merged_files.xlsx", max_rows=1000000):
    """
    安全的xlsx文件合并函数，当数据过大时分割成多个工作表

    参数:
    - folder_path: 文件夹路径
    - output_name: 输出文件名
    - max_rows: 每个工作表最大行数（默认100万，留一些余量）
    """

    # 忽略openpyxl警告
    warnings.filterwarnings('ignore')

    # 获取所有xlsx文件
    excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    excel_files.sort()  # 按文件名排序

    if not excel_files:
        print("没有找到xlsx文件")
        return

    print(f"找到 {len(excel_files)} 个xlsx文件")

    # 第一步：读取所有文件数据
    all_data = []
    total_rows = 0

    for i, file in enumerate(excel_files, 1):
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_excel(file_path)
            df['来源文件'] = file  # 添加来源文件列
            all_data.append(df)
            total_rows += len(df)
            print(f"[{i}/{len(excel_files)}] 已添加: {file} (共{len(df)}行)")
        except Exception as e:
            print(f"警告: 无法读取文件 {file}: {e}")

    if not all_data:
        print("没有成功读取任何文件数据")
        return

    # 合并所有数据
    merged_df = pd.concat(all_data, ignore_index=True)
    print(f"\n数据合并完成！")
    print(f"总文件数: {len(excel_files)}")
    print(f"总数据行数: {total_rows}")
    print(f"总数据列数: {len(merged_df.columns)}")

    # 第二步：检查是否需要分割
    if total_rows <= max_rows:
        # 不需要分割，直接保存
        output_path = os.path.join(folder_path, output_name)
        merged_df.to_excel(output_path, index=False)
        print(f"\n合并完成！保存到: {output_path}")
    else:
        # 需要分割成多个工作表
        num_sheets = (total_rows // max_rows) + 1
        print(f"\n数据量过大，将分割成 {num_sheets} 个工作表")
        print(f"每个工作表最多 {max_rows} 行")

        # 创建Excel写入器
        output_path = os.path.join(folder_path, output_name)
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_num in range(num_sheets):
                # 计算当前工作表的起始和结束位置
                start_row = sheet_num * max_rows
                end_row = min((sheet_num + 1) * max_rows, total_rows)

                # 分割数据
                sheet_df = merged_df.iloc[start_row:end_row].copy()

                # 添加工作表信息
                sheet_df['工作表序号'] = sheet_num + 1

                # 写入工作表
                sheet_name = f"Sheet{sheet_num + 1}"
                sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

                print(f"已写入工作表 {sheet_name}: 行 {start_row + 1}-{end_row}")

        print(f"\n合并完成！保存到: {output_path}")
        print(f"共 {num_sheets} 个工作表")

    # 显示列信息
    print("\n列名列表:")
    for i, col in enumerate(merged_df.columns, 1):
        print(f"{i:2d}. {col}")


def advanced_merge_excel(folder_path, output_name="merged_files.xlsx",max_rows=1000000, separate_by_source=False):
    """
    高级合并函数，提供更多选项

    参数:
    - folder_path: 文件夹路径
    - output_name: 输出文件名
    - max_rows: 每个工作表最大行数
    - separate_by_source: 是否按来源文件分割（True时，每个文件一个工作表）
    """

    warnings.filterwarnings('ignore')

    # 获取所有xlsx文件
    excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    excel_files.sort()

    if not excel_files:
        print("没有找到xlsx文件")
        return

    print(f"找到 {len(excel_files)} 个xlsx文件")

    # 按来源文件分割的模式
    if separate_by_source:
        print("\n使用按来源文件分割模式")
        output_path = os.path.join(folder_path, output_name)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, file in enumerate(excel_files, 1):
                file_path = os.path.join(folder_path, file)
                try:
                    df = pd.read_excel(file_path)
                    # 截断工作表名称（Excel限制31字符）
                    sheet_name = file[:31] if len(file) > 31 else file
                    sheet_name = sheet_name.replace('.xlsx', '')

                    # 如果数据过大，分割成多个工作表
                    if len(df) > max_rows:
                        num_sheets = (len(df) // max_rows) + 1
                        for sheet_num in range(num_sheets):
                            start_row = sheet_num * max_rows
                            end_row = min((sheet_num + 1) * max_rows, len(df))
                            sheet_df = df.iloc[start_row:end_row]

                            sub_sheet_name = f"{sheet_name}_part{sheet_num + 1}"[:31]
                            sheet_df.to_excel(writer, sheet_name=sub_sheet_name, index=False)
                            print(f"[{i}/{len(excel_files)}] {file} -> {sub_sheet_name}: 行 {start_row + 1}-{end_row}")
                    else:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"[{i}/{len(excel_files)}] {file} -> {sheet_name}: 共{len(df)}行")

                except Exception as e:
                    print(f"警告: 无法读取文件 {file}: {e}")

        print(f"\n合并完成！保存到: {output_path}")
        return

    # 默认模式：合并所有数据
    safe_merge_excel(folder_path, output_name, max_rows)


# 使用示例
if __name__ == "__main__":
    # 选择一个文件夹
    folders = [
        # r"C:\Users\Airkoy\Desktop\知乎_zvideo",
        # r"C:\Users\Airkoy\Desktop\知乎_articles",
        # r"C:\Users\Airkoy\Desktop\知乎_questions",
        r"C:\Users\Airkoy\Desktop\知乎_pins"
    ]

    for folder in folders:
        if os.path.exists(folder):
            print(f"\n{'=' * 60}")
            print(f"处理文件夹: {folder}")
            print('=' * 60)

            # 方法1: 简单合并，自动分割
            safe_merge_excel(folder, "merged_files.xlsx")

            # 方法2: 高级合并，按来源文件分割
            # advanced_merge_excel(folder, "merged_by_source.xlsx", separate_by_source=True)

            print(f"\n文件夹 {os.path.basename(folder)} 处理完成！")
        else:
            print(f"文件夹不存在: {folder}")