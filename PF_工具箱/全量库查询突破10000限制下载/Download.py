import requests
import os
from datetime import datetime

# 该代码仅试验，用于小于10000的一次性下载任务
# 小于1w的话，不如直接手动在全量库查询下载

url = 'https://dc.datastory.com.cn/banyan/downloadBanyanTabData'

headers = {
    "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc2NDIyODY4MjAxNSwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NjQ4MzM0ODJ9.1xtkdeDKIZ6TGYi2vMMFM_Eez7XD3E1aQa6k35X0gtgpMUAKRR0UFuw2af18MQbAP4OBLD2QDLIcJ-3mT_djBg",
    "Content-Type": "application/json",
    "Priority": "u=1, i",  # u这里应该是页面上提交的命名
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
}

# 请求数据 -
data = {
    "dataType": "GlobalMedia",
    "banyanType": "elf",
    "searchType": "Post",
    "fileName": "1",
    "needReturnFields": "id,item_id,site_id,site_name,url",
    "searchCondition": [
        {
            "fieldName": "site_name",
            "operation": "mp",
            "fieldValue": ["YouTube|YouTube_shorts", ""]
        },
        {
            "fieldName": "publish_timestamp",
            "operation": "ltegte",
            # "fieldValue": [1740758400000, 1748966399000]
            "fieldValue": [1740758400000, 1764172799000]
        }

    ],
    "sortCondition": {
        "sortFieldName": "publish_timestamp",
        "order": "desc"
    },
}

# "fieldValue": [1740758400000, 1764172799000]  原始时间线

# 发送POST请求
try:
    response = requests.post(url, headers=headers, json=data)

    # 打印响应状态
    print(f"状态码: {response.status_code}")
    print(response.headers)
    # print(response.content)
    # print(response.text)

    # 从数据中提取时间范围
    start_timestamp = data["searchCondition"][1]["fieldValue"][0]
    end_timestamp = data["searchCondition"][1]["fieldValue"][1]

    if response.headers.get('Content-Type') == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8':

        print("请求成功")
        # 指定保存目录和文件名
        save_directory = r"C:\Users\Airkoy\Desktop\新建文件夹"  # Windows路径

        # 确保目录存在
        os.makedirs(save_directory, exist_ok=True)

        filename = f"数据_{start_timestamp}-{end_timestamp}.xlsx"

        # 完整的文件路径
        full_path = os.path.join(save_directory, filename)

        # # 保存文件
        # with open(full_path, 'wb') as f:
        #     f.write(response.content)

        print(f"Excel文件已保存到: {full_path}")

    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.headers.get('Content-Type'))
        print(response.text)
        # print(response.text)


except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")

# 错误响应：
# 状态码: 200
# 响应头: {'Server': 'nginx', 'Date': 'Thu, 27 Nov 2025 09:20:56 GMT', 'Content-Type': 'application/json;charset=UTF-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block', 'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0', 'X-Frame-Options': 'DENY', 'X-Application-Context': 'application:devops:32135', 'X-Tr': 'e00afa4930754455bf77b46419b8a0b3.68383270.17642352559620079', 'Content-Encoding': 'gzip'}
# 请求成功!
# 响应数据: {'message': '该任务数据量为：150200,超过了10000,减少数据量再创建任务', 'success': False, 'code': -1, 'data': None}

# 状态码: 200
# 响应头: {'Server': 'nginx', 'Date': 'Thu, 27 Nov 2025 09:24:04 GMT', 'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block', 'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0', 'X-Frame-Options': 'DENY', 'X-Application-Context': 'application:devops:32135', 'X-Tr': '4734d39d1cb342a3a92d213629ab0d33.68414843.17642354315070041', 'Content-Disposition': 'attachment;filename=1.xlsx'}
# 请求成功!
