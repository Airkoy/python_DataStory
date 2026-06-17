
import pandas as pd
from datetime import datetime

# 读取Excel文件
df = pd.read_excel(r"C:\Users\Airkoy\Desktop\睿符小红书主帖数据推送.xlsx")
print(df.columns.tolist())