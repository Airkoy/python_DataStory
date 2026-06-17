import pandas as pd


def extract_duplicates(input_csv, output_csv, check_columns=None):
    """
    检查CSV中的重复数据，并输出到新文件

    :param input_csv: 输入的CSV文件路径
    :param output_csv: 输出的重复数据CSV文件路径
    :param check_columns: 检查重复的列名列表。如果为None，则检查整行是否完全一致
    """
    # 【修改1】强制指定 dtype，将 item_id 读取为字符串，消除警告并避免后续类型冲突
    # 如果你还有其他列也有类型混合问题，也可以加在字典里，如 {'item_id': str, 'is_origin': str}
    dtype_dict = {'item_id': str}

    # 读取数据，指定 dtype 解决 DtypeWarning
    df = pd.read_csv(input_csv, encoding='utf-8-sig', dtype=dtype_dict)

    # 确定 keep=False 非常关键
    if check_columns is None:
        duplicates = df[df.duplicated(keep=False)]
        print(f"基于【整行数据】检查，共发现 {len(duplicates)} 条涉及重复的记录。")
    else:
        duplicates = df[df.duplicated(subset=check_columns, keep=False)]
        print(f"基于列 {check_columns} 检查，共发现 {len(duplicates)} 条涉及重复的记录。")

    if duplicates.empty:
        print("没有发现重复数据，无需输出。")
        return

    # 按照检查的列进行排序
    sort_by = check_columns if check_columns is not None else list(df.columns)

    # 【修改2】排序前，将用于排序的列强制转为字符串，确保排序时不会发生 str 与 int 比较的报错
    duplicates_sorted = duplicates.copy()
    for col in sort_by:
        duplicates_sorted[col] = duplicates_sorted[col].astype(str)

    duplicates_sorted = duplicates_sorted.sort_values(by=sort_by)

    # 保存到新的CSV文件
    duplicates_sorted.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"重复数据已输出到: {output_csv}")


# ================= 使用示例 =================
if __name__ == '__main__':
    input_file = 'weibo_post_by_uid.csv'
    output_file = 'duplicates_output_byuid_仅item_id.csv'

    # 仅根据 item_id 检查重复
    extract_duplicates(input_file, output_file, check_columns=['item_id'])