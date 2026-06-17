import requests
import json
from typing import Dict, Optional


def get_token(username: str, password: str, url: str = 'https://dc.datastory.com.cn/auth/obtain') -> Optional[str]:
    """
  获取token的函数

  参数:
  username: 用户名
  password: 密码
  url: 认证URL

  返回:
  token字符串，失败返回None
  """
    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # 检查请求是否成功

        if response.status_code == 200:
            response_data = response.json()
            if 'data' in response_data:
                return response_data['data']
            else:
                print(f"响应中没有找到token: {response.text}")
                return None
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"解析JSON响应失败: {e}")
        return None


def load_accounts(filename: str = 'accounts.json') -> Dict:
    """
  从文件加载账号信息

  参数:
  filename: 文件名

  返回:
  账号字典
  """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            accounts = json.load(f)
        print(f"从 {filename} 加载了 {len(accounts)} 个账号")
        return accounts
    except (json.JSONDecodeError, IOError) as e:
        print(f"读取文件失败: {e}")
        return {}


def get_token_by_name(account_name: str, filename: str = 'accounts.json') -> tuple:
    accounts = load_accounts(filename)

    if account_name not in accounts:
        print(f"错误: 未找到账号 '{account_name}'")
        return None, None, None

    account_info = accounts[account_name]
    username = account_info['username']
    password = account_info['password']

    print(f"正在为 '{account_name}' 获取token...")
    token = get_token(username, password)
    return account_name, token


def create_new_folder(folder_name, folder_token):
    folder_headers = {
        'Content-Type': 'application/json',
        'Authorization': folder_token,
    }
    # folder_url = f"http://dc.dev.datastory.com.cn/sheet/add?name={folder_name}"
    folder_url = f"https://dc.datastory.com.cn/sheet/add?uuu=banyan&name={folder_name}"
    response = requests.request("POST", folder_url, headers=folder_headers)

    if not response.json()['success']:
        print("已存在重复文件夹")
    else:
        print("sheetId:", response.json()['data'])
        return response.json()['data']


# url = "https://dc.datastory.com.cn/sheet/add?uuu=banyan&name=新的文件夹"

new_folder_name = "板块名称-互动量更新test"
account_name, referred_token = get_token_by_name("koy账号")
response = create_new_folder(new_folder_name, referred_token)
print(response.text)
print(response.json()['data'])
print(response.json()['success'])

if not response.json()['success']:
    print("已存在重复文件夹")
else:
    print("sheetId:",response.json()['data'])
