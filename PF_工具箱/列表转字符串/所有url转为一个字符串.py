import json
import os


def _read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def _parse_content(content):
    stripped = content.strip()
    try:
        data = json.loads(stripped)
    except json.JSONDecodeError:
        pass
    else:
        if isinstance(data, list):
            return ','.join(str(item) for item in data)
        return str(data)

    lines = (line.rstrip('\n').rstrip('\r') for line in stripped.splitlines())
    return ','.join(line for line in lines if line)


def json_to_comma_string(file_path):
    """
    读取 JSON 文件，将每一行（或每个元素）的数据用逗号拼接成一个字符串返回。

    支持两种 JSON 格式：
      1. JSON 数组：[value1, value2, ...]
      2. JSON Lines（每行一个 JSON 值）
    """
    content = _read_file(file_path)
    return _parse_content(content)


# ========== 使用示例 ==========
#
# # 示例 1：JSON 数组文件
# # data.json 内容: ["apple", "banana", "cherry"]
# result = json_to_comma_string('data.json')
# print(result)  # 输出: apple,banana,cherry

# 示例 2：JSON Lines 文件
# data.jsonl 内容:
#   "apple"
#   "banana"
#   "cherry"

# 示例 3：JSON 数组中含对象
# data.json 内容: [{"id":1,"name":"A"}, {"id":2,"name":"B"}]
# result = json_to_comma_string('data.json')
# print(result)  # 输出: {'id': 1, 'name': 'A'},{'id': 2, 'name': 'B'}

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, 'data.json')
    result = json_to_comma_string(path)
    print(result)

