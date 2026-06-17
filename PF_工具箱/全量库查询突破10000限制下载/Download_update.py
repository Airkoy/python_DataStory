import requests
import os
import time
from datetime import datetime
import json


class DataDownloader:
    def __init__(self, config=None):
        # 默认配置
        default_config = {
            "url": 'https://dc.datastory.com.cn/banyan/downloadBanyanTabData',
            "headers": {
                "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc2NDIyODY4MjAxNSwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NjQ4MzM0ODJ9.1xtkdeDKIZ6TGYi2vMMFM_Eez7XD3E1aQa6k35X0gtgpMUAKRR0UFuw2af18MQbAP4OBLD2QDLIcJ-3mT_djBg",
                "Content-Type": "application/json",
                "Priority": "u=1, i",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.8",
            },
            "save_directory": r"C:\Users\Airkoy\Desktop\新建文件夹",
            "data_template": {
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
                        "fieldValue": [1740758400000, 1764172799000]  # 会被实际时间范围替换
                    }
                ],
                "sortCondition": {
                    "sortFieldName": "publish_timestamp",
                    "order": "desc"
                },
            },
            "start_timestamp": 1740758400000,  # 2025-03-01
            "end_timestamp": 1764172799000,  # 2025-11-27
            "max_attempts": 10,  # 最大递归深度，防止无限循环
            "delay_between_requests": 1  # 请求间隔时间(秒)
        }

        # 合并用户配置和默认配置
        if config:
            self.config = self._merge_configs(default_config, config)
        else:
            self.config = default_config

        # 设置实例变量以便访问
        self.url = self.config["url"]
        self.headers = self.config["headers"]
        self.save_directory = self.config["save_directory"]
        self.data_template = self.config["data_template"]
        self.max_attempts = self.config["max_attempts"]
        self.delay_between_requests = self.config["delay_between_requests"]

    def _merge_configs(self, default, user):
        """递归合并默认配置和用户配置"""
        result = default.copy()
        for key, value in user.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def timestamp_to_date(self, timestamp):
        """将时间戳转换为可读日期"""
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

    def download_data(self, start_timestamp, end_timestamp, attempt=1):
        """
        使用二分法下载数据
        """
        if attempt > self.max_attempts:
            print(f"达到最大递归深度 {self.max_attempts}，停止拆分")
            return False

        print(
            f"\n尝试 #{attempt}: 时间范围 {self.timestamp_to_date(start_timestamp)} 到 {self.timestamp_to_date(end_timestamp)}")

        # 创建数据副本并设置时间范围
        data = self.data_template.copy()
        # 更新时间范围字段
        for condition in data["searchCondition"]:
            if condition["fieldName"] == "publish_timestamp":
                condition["fieldValue"] = [start_timestamp, end_timestamp]
                break

        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            # print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')

                if content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8':
                    # 成功下载Excel文件
                    os.makedirs(self.save_directory, exist_ok=True)
                    filename = f"数据_{start_timestamp}-{end_timestamp}_{self.timestamp_to_date(start_timestamp)}_to_{self.timestamp_to_date(end_timestamp)}.xlsx"
                    full_path = os.path.join(self.save_directory, filename)

                    with open(full_path, 'wb') as f:
                        f.write(response.content)

                    print(f"✓ 成功下载: {filename}")
                    return True

                else:
                    # 解析错误信息
                    try:
                        error_data = response.json()
                        if "超过了10000" in error_data.get("message", ""):
                            print(f"数据量过大 ({error_data['message']})，开始二分拆分...")

                            # 计算中间时间点
                            mid_timestamp = (start_timestamp + end_timestamp) // 2

                            # 添加请求间隔
                            time.sleep(self.delay_between_requests)

                            # 递归调用：拆分前半部分
                            success1 = self.download_data(start_timestamp, mid_timestamp, attempt + 1)

                            # 添加请求间隔
                            time.sleep(self.delay_between_requests)

                            # 递归调用：拆分后半部分
                            success2 = self.download_data(mid_timestamp + 1, end_timestamp, attempt + 1)

                            return success1 and success2

                        else:
                            print(f"其他错误: {error_data.get('message', '未知错误')}")
                            return False

                    except json.JSONDecodeError:
                        print(f"响应解析失败: {response.text}")
                        return False
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return False

    def start_download(self, start_timestamp=None, end_timestamp=None):
        """开始下载过程"""
        print("开始数据下载任务...")
        print("=" * 50)

        # 使用配置的时间范围或传入的参数
        if start_timestamp is None:
            start_timestamp = self.config["start_timestamp"]
        if end_timestamp is None:
            end_timestamp = self.config["end_timestamp"]

        print(f"时间范围: {self.timestamp_to_date(start_timestamp)} 到 {self.timestamp_to_date(end_timestamp)}")

        success = self.download_data(start_timestamp, end_timestamp)

        if success:
            print("\n✓ 所有数据下载完成!")
        else:
            print("\n✗ 部分数据下载失败，请检查日志")

        print("=" * 50)


# 使用示例
if __name__ == "__main__":
    # 自定义配置，主要的参数都可以在这里进行配置，主要使用的是二分法，去把完整的时间拆分成多个任务进行下载
    # 这里只写了下载，没写合并文件
    # 最少需要传入 Authorization save_directory dataType needReturnFields searchCondition startTimestamp endTimestamp
    custom_config = {
        "headers": {
            "Authorization": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc2NTQzNDY1NzY4OCwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NjYwMzk0NTd9.9tgwCUW0SynAl0v6z52JkcthntaVJ9b2RYqe9froryjC2N1p9t6pmbJkZ-BeViWoCRIPVqlnYans4XReTQghDw",
            "Content-Type": "application/json",
            "Priority": "u=1, i",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.8",
        },
        "save_directory": r"C:\Users\Airkoy\Desktop\知乎_pins",  # 本地保存地址
        "data_template": {
            "dataType": "NewsForum",  # 数据源 NewsForum-->新闻论坛 GlobalMedia-->海外社媒
            "banyanType": "elf",
            "searchType": "Post",  # 查询内容选择“主帖”
            # "searchType":"User",  # 查询内容选择“用户信息”
            "fileName": "pins",
            "needReturnFields": "site_id,site_name,site_source_ids,site_source_names,url",  # 需要展示的字段
            "searchCondition": [
                {"fieldName": "site_id", "operation": "eq", "fieldValue": ["101944"]},
                {"fieldName": "post_type", "operation": "eq", "fieldValue": ["pins"]},
                # {"fieldName": "site_name", "operation": "mp", "fieldValue": ["新浪汽车",""]},
                {"fieldName": "publish_timestamp", "operation": "ltegte", "fieldValue": [1735660800000, 1765727999000]},
            ],
            "sortCondition": {
                "sortFieldName": "update_timestamp",
                "order": "desc"
            },
        },


        "start_timestamp": 1735660800000,  # 2025-xx-xx

        "end_timestamp": 1765727999000,  # 2025-xx-xx
        "max_attempts": 20,  # 最大二分次数
        "delay_between_requests": 1  # 每次请求延迟时间，当前为1s
    }

    # 创建下载器实例
    downloader = DataDownloader(custom_config)

    # 开始下载
    downloader.start_download()

    # 或者使用自定义时间范围
    # downloader.start_download(1740758400000, 1751500800000)
