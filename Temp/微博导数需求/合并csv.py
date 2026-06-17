import csv

# 定义文件路径
file1 = 'weibo_post_by_uid.csv'
file2 = 'weibo_post_by_pgc.csv'
output_file = 'merged_output.csv'

with open(output_file, 'w', newline='', encoding='utf-8') as out_f:
    writer = csv.writer(out_f)

    # 1. 读取并写入第一个文件的全部内容（包含表头）
    with open(file1, 'r', newline='', encoding='utf-8') as f1:
        reader1 = csv.reader(f1)
        for row in reader1:
            writer.writerow(row)

    # 2. 读取并写入第二个文件的内容（跳过表头）
    with open(file2, 'r', newline='', encoding='utf-8') as f2:
        reader2 = csv.reader(f2)
        next(reader2)  # 跳过第二份文件的表头
        for row in reader2:
            writer.writerow(row)

print("合并完成！文件已保存为:", output_file)