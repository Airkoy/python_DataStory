import json
import pandas as pd

json_data = '''
[
  {"站点名称": "微博", "区域": "-", "site_id": "101993", "scope_id": "4", "app_id": "6"},
  {"站点名称": "微信公众号", "区域": "-", "site_id": "102027", "scope_id": "10", "app_id": "7"},
  {"站点名称": "抖音", "区域": "短视频", "site_id": "1003583", "scope_id": "7", "app_id": "8"},
  {"站点名称": "豆瓣", "区域": "小组", "site_id": "101945", "scope_id": "1", "app_id": "9"}
  // ... (将上方完整的JSON数组粘贴至此处替换) ...
]
'''

# 解析JSON
data = json.loads(json_data)

# 转换为Pandas DataFrame
df = pd.DataFrame(data, columns=["站点名称", "区域", "site_id", "scope_id", "app_id"])

# 导出为Excel文件
output_file = "聚合-数据超市站点区域信息_提取版.xlsx"
df.to_excel(output_file, index=False)

print(f"成功导出Excel文件：{output_file}")