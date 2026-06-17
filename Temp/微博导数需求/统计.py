import pandas as pd


def count_specific_items(csv_file):
    # 读取CSV文件
    df = pd.read_csv(csv_file)

    limit = 100
    # 构建三个筛选条件 (注意：每个条件需要用括号括起来)
    # cond_repost = (df['repost_cnt'] > 0) & (df['repost_cnt'] < 10)
    # cond_like = (df['like_cnt'] > 0) & (df['like_cnt'] < 10)
    # cond_comment = (df['comment_cnt'] >= 10) & (df['comment_cnt'] < 10)
    cond_repost = (df['repost_cnt'] >= limit)
    cond_like = (df['like_cnt'] >= limit)
    cond_comment = (df['comment_cnt'] >= limit)

    # 应用条件，筛选出同时满足三个条件的行
    filtered_df = df[cond_repost & cond_like & cond_comment]
    # filtered_df = df[cond_comment]

    # 统计满足条件的 item_id 数量
    # 方式1：直接统计满足条件的行数（假设每行对应一个唯一的item_id）
    count_by_rows = len(filtered_df)

    # 方式2：统计满足条件的 唯一 item_id 数量（如果数据中有重复的item_id）
    count_by_unique = filtered_df['item_id'].nunique()

    print(f"满足条件的记录数: {count_by_rows}")
    print(f"满足条件的唯一item_id数: {count_by_unique}")

    return count_by_rows


# 调用函数
if __name__ == '__main__':
    # 替换为你的实际csv文件路径
    input_csv = 'merged_output.csv'
    count_specific_items(input_csv)

# 评论 > =10
# 满足条件的记录数: 773690
# 满足条件的唯一item_id数: 700761
#
# 评论 >=50
# 满足条件的记录数: 351460
# 满足条件的唯一item_id数: 320135
#
# 评论 >=100
# 满足条件的记录数: 245905
# 满足条件的唯一item_id数: 224620

# 转赞评 >=3
# 满足条件的记录数: 865650
# 满足条件的唯一item_id数: 781290

# 转赞评 >=10
# 满足条件的记录数: 495682
# 满足条件的唯一item_id数: 450574

# 转赞评 >=50
# 满足条件的记录数: 230984
# 满足条件的唯一item_id数: 210708

# 转赞评 >=100
# 满足条件的记录数: 161554
# 满足条件的唯一item_id数: 147406







