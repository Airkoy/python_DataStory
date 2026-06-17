import requests
import json
import pandas as pd
from datetime import datetime
import os


def read_names_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        # 读取所有行，去除每行首尾的空白字符（包括换行符）
        names = [line.strip() for line in f if line.strip()]
    return names


def get_weixin_uid(headers, data):
    url = 'https://dc.datastory.com.cn/monitor/account/wechatVideo/batchSearch?uuu=banyan'
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()['data']
    return response_data


def print_item(data):
    for item in data['uids']:
        print(f"账号名称: {item['nickName']}, 视频号: {item['uid']}")


def out_to_excel(data, excel_filename):
    excel_data = []
    for item in data['uids']:
        excel_data.append({
            '账号名称': item['nickName'],
            '视频号': item['uid']
        })

    # 创建DataFrame
    df = pd.DataFrame(excel_data)

    save_dir = r'D:\python_project\python_DataStory\微信视频号查询记录'
    export_file = os.path.join(save_dir, excel_filename)
    # 保存到Excel文件

    df.to_excel(export_file, index=False, sheet_name='sheet1')
    print(f"\nExcel文件已创建: {excel_filename}")

    # 可选：同时输出统计信息
    print(f"\n总共找到 {len(data['uids'])} 个账号")


def transfer_data(data):
    accounts_list = []
    for item in data['uids']:
        accounts_list.append({
            'name': item['nickName'],
            'uid': item['uid']
        })
    result = {
        'accounts': accounts_list
    }
    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    # print("转换后的JSON:")
    # print(json_str)
    return json_str


def add_monitor(headers, add_monitor_data):
    url = "https://dc.datastory.com.cn/monitor/account/wechatVideo/add?uuu=banyan"
    response_of_add_monitor = requests.post(url, headers=headers, data=add_monitor_data)
    print(response_of_add_monitor.text)


if __name__ == "__main__":
    Headers = {
        "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJoZXJtZXNfYWRtaW5AZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc4MTU4MTI0MzAzMSwicHciOiJoU204VzJNbXVIeT9KQCFOek0yVCIsImV4cCI6MTc4MjE4NjA0M30.e1VOeZahPGrZtN1N7x29xDyr_r9VJuzauMTU1H5pqwIuJBU7x9YyYnXEsuP3FWpQ_P7oG1YNm4wPSJMtc-V0FQ",
        "Content-Type": "application/json"
    }
    requests_data = {
        "name": read_names_from_file('weixin_uid.json')
    }
    now = datetime.now()
    now.strftime("%Y年%m月%d日 %H时%M分%S秒")
    save_dir = r'D:\python_project\python_DataStory\微信视频号查询记录'

    excel_filename = f'视频号查询_{now.strftime("%Y年%m月%d日 %H时%M分%S秒")}.xlsx'

    # 获取uid，导出到excel
    response_data = get_weixin_uid(Headers, requests_data)  # 根据昵称获取uid
    # print_item(response_data)  # 打印账号名称、uid
    out_to_excel(response_data, excel_filename)  # 导出到excel

    # 提交需要监控的账号
    monitor_data = transfer_data(response_data)
    # print(monitor_data)
    add_monitor(Headers, monitor_data)
