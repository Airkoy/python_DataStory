import datetime


def yyyymmddhhmmss_to_timestamp(time_str):
    """将 yyyymmddhhmmss 格式转换为时间戳"""
    dt = datetime.datetime.strptime(time_str, "%Y%m%d%H%M%S")
    return int(dt.timestamp()*1000)


# 使用示例
if __name__ == "__main__":
    time_list = ["20260617150000", "20260617235959"]
    timestamp = [yyyymmddhhmmss_to_timestamp(t) for t in time_list]
    print(timestamp)