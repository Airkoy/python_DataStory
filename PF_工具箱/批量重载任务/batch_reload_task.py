import requests
import json
from typing import Dict, Optional


# 该代码能够通过输入测试环境（新架构目前测试支持）的jobId，实现在生产环境起相同任务，达到快速测试的效果 ---> by koy 20260206

# 局限1：当前run_datamarket_job()函数里，admin_headers 和 auth_headers 是一样的
# 本意为 通过admin_token查所有任务，通过修改auth_token能够实现在任意账号下起任务，但admin在这个接口没有随便查询的权限，只能作罢
# 当前只能用在测试环境起任务的用户token进行查询，但仍可通过修改auth_token能够实现在任意账号下起任务

# 局限2：当前只能保存到本地，方舟的参数目前不知道咋整，待研究

# 局限3：需要先到生产环境，创建、保存一个任务，然后通过api示例功能拿到sheetId -> 已解决，可通过create_sheetId.py创建文件夹0209

# 局限4：不能通过保存的账号密码，自动获取token -> 嗯…… 可开发，思考要不要 ->已开发0209


def run_datamarket_job(url_id, sheet_id, export_config=None, query_url=None, query_token=None, run_task_url=None,
                       run_task_token=None):
    """
    执行数据市场任务的函数

    参数:
    url_id: test_url末尾的id参数值（URL中的id）
    sheet_id: new_requestData['sheetId']的值
    export_config: new_requestData['exportConfig']的值，默认为{'local': {}}
    prod_url: 生产环境URL，默认使用提供的URL
    auth_token: 认证token，默认使用提供的token
    """
    # 设置默认值
    if export_config is None:
        export_config = {'local': {}}

    export_config = {'local': {}}

    query_user_headers = {
        'Content-Type': 'application/json',
        'Authorization': query_token,
    }

    run_task_headers = {
        'Content-Type': 'application/json',
        'Authorization': run_task_token,
    }

    # 第一步：发送GET请求获取数据
    # 注意：这里没有payload了，或者payload中不需要id参数
    payload = json.dumps({})  # 空payload，或者根据实际情况调整

    try:
        print(f"正在获取数据 (URL ID: {url_id})...")
        print(f"请求URL: {query_url}")
        response = requests.request("GET", query_url, headers=query_user_headers,
                                    data=payload)  # 生产环境的查询，可以用admin查所有，测试环境只能自查
        response.raise_for_status()  # 检查请求是否成功
        response_data = response.json()
        print("数据获取成功")
        # print(response_data)
    except requests.exceptions.RequestException as e:
        print(f"获取数据失败: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"解析JSON响应失败: {e}")
        return None

    # 第二步：准备新的请求数据
    if 'data' not in response_data:
        print("响应数据中没有找到'data'字段")
        return None

    new_requestData = response_data['data']
    if new_requestData is None:
        print(f"响应数据中'data'字段为None，可能该任务不存在或无权限访问 (URL ID: {url_id})")
        return None

    new_requestData['exportConfig'] = export_config
    new_requestData['sheetId'] = sheet_id
    new_requestData["workflowId"] = ''

    # 第三步：发送POST请求到 创建任务的接口
    try:
        response2 = requests.post(run_task_url, data=json.dumps(new_requestData), headers=run_task_headers)
        print(response2.text)
        return response2.text
    except requests.exceptions.RequestException as e:
        print(f"发送POST请求失败: {e}")
        return None
    except json.JSONDecodeError:
        # 如果响应不是JSON格式，直接返回文本
        return response2.text


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


def load_accounts(filename: str = r'D:\python_project\python_DataStory\PF_工具箱\批量重载任务\accounts.json') -> Dict:
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
    return token


def create_new_folder(folder_name, folder_token, folder_path):
    print("正在创建新文件夹")
    folder_headers = {
        'Content-Type': 'application/json',
        'Authorization': folder_token,
    }
    if folder_path == "dev":
        folder_url = f"http://dc.dev.datastory.com.cn/sheet/add?name={folder_name}"
    else:
        folder_url = f"https://dc.datastory.com.cn/sheet/add?uuu=banyan&name={folder_name}"

    response = requests.request("POST", folder_url, headers=folder_headers)

    if not response.json()['success']:
        print("已存在重复文件夹，开始查询文件夹id")
        target_forlder_id = query_folder_id(folder_token, folder_name, folder_path)
        return target_forlder_id
    else:
        print("sheetId:", response.json()['data'])
        return response.json()['data']


def query_folder_id(run_task_token, target_name, folder_path):
    if folder_path == "dev":
        url_test_datamarket = "http://dc.dev.datastory.com.cn/sheet/list?uuu=banyan"
    else:
        url_test_datamarket = "https://dc.datastory.com.cn/sheet/list?uuu=banyan"
    payload = json.dumps({})
    headers = {
        "Authorization": run_task_token,
        "Content-Type": "application/json"
    }
    response = requests.request("GET", url_test_datamarket, headers=headers, data=payload)
    response.raise_for_status()  # 检查HTTP请求是否成功
    response_data = response.json()

    # 检查返回状态并提取id
    if response_data.get("success") and "data" in response_data:
        # target_name = "20260305版本测试"
        found_id = None

        for item in response_data["data"]:
            if item.get("name") == target_name:
                found_id = item.get("id")
                break

        if found_id:
            print(f'任务名称 "{target_name}" 对应的ID是: {found_id}')
            return found_id
        else:
            print(f'未找到名称为 "{target_name}" 的任务。')

    else:
        print("接口返回失败或数据格式异常：", response_data.get("message"))


def choose_action(source, target, url_ids, query_token, run_task_token, target_folder_name):
    if source == "dev" and target == "prod":
        print("正在运行 dev to prod")
        sheet_id = create_new_folder(target_folder_name, run_task_token, "")
        for url_id in url_ids:
            print(f"\n{'=' * 50}")
            print(f"处理任务 (URL ID: {url_id})")
            print(f"{'=' * 50}")
            query_url_dev = f"http://dc.dev.datastory.com.cn/application/market/job/v1/detail?id={url_id}"
            run_task_url_prod = "https://dc.datastory.com.cn/application/market/job/v1/run"  # 生产环境，创建任务
            result = run_datamarket_job(url_id, sheet_id, export_config=None,
                                        query_url=query_url_dev, query_token=query_token,
                                        run_task_url=run_task_url_prod, run_task_token=run_task_token)

    if source == "dev" and target == "dev":
        print("正在运行 dev to dev")
        sheet_id = create_new_folder(target_folder_name, run_task_token, "dev")
        for url_id in url_ids:
            print(f"\n{'=' * 50}")
            print(f"处理任务 (URL ID: {url_id})")
            print(f"{'=' * 50}")
            query_url_dev = f"http://dc.dev.datastory.com.cn/application/market/job/v1/detail?id={url_id}"
            run_task_url_dev = "http://dc.dev.datastory.com.cn/application/market/job/v1/run"  # 测试环境 创建任务
            result = run_datamarket_job(url_id, sheet_id, export_config=None,
                                        query_url=query_url_dev, query_token=query_token,
                                        run_task_url=run_task_url_dev, run_task_token=run_task_token)

    if source == "prod" and target == "dev":
        print("正在运行 prod to dev")
        sheet_id = create_new_folder(target_folder_name, run_task_token, "dev")
        for url_id in url_ids:
            print(f"\n{'=' * 50}")
            print(f"处理任务 (URL ID: {url_id})")
            print(f"{'=' * 50}")
            query_url_prod = f"https://dc.datastory.com.cn/application/market/job/v1/detail?id={url_id}&uuu=banyan"
            run_task_url_dev = "http://dc.dev.datastory.com.cn/application/market/job/v1/run"  # 测试环境 创建任务
            result = run_datamarket_job(url_id, sheet_id, export_config=None,
                                        query_url=query_url_prod, query_token=query_token,
                                        run_task_url=run_task_url_dev, run_task_token=run_task_token)

    if source == "prod" and target == "prod":
        print("正在运行 prod to prod")
        sheet_id = create_new_folder(target_folder_name, run_task_token, "")
        for url_id in url_ids:
            print(f"\n{'=' * 50}")
            print(f"处理任务 (URL ID: {url_id})")
            print(f"{'=' * 50}")
            query_url_prod = f"https://dc.datastory.com.cn/application/market/job/v1/detail?id={url_id}&uuu=banyan"
            run_task_url_prod = "https://dc.datastory.com.cn/application/market/job/v1/run"  # 生产环境，创建任务
            result = run_datamarket_job(url_id, sheet_id, export_config=None,
                                        query_url=query_url_prod, query_token=query_token,
                                        run_task_url=run_task_url_prod, run_task_token=run_task_token)


if __name__ == "__main__":
    # sheet_default = 1093  # 旧配置，万一下面自动拿文件夹id函数时效可以用 koy 260205版本测试文件夹  56884 HERMES-7632文件夹  62123 20260305版本测试

    # exportConfig_default = {'local': {}} # 默认的保存配置，可不传

    # run_task_url_prod = "https://dc.datastory.com.cn/application/market/job/v1/run"  # 生产环境，创建任务
    # run_task_url_dev = "http://dc.dev.datastory.com.cn/application/market/job/v1/run"  # 测试环境 创建任务

    # 输入jobId
    # url_ids = [17640400,17640362,]
    url_ids = [55315,55314,55313,55310,55312,55305,55309,55308,55307,55306,55304,55303,55316]

    query_token = get_token_by_name("koy账号")
    run_task_token = get_token_by_name("koy账号")

    target_folder_name = "20260616版本测试"
    # sheet_id = create_new_folder(target_folder_name, run_task_token, "dev")  # 测试环境的文件夹就“dev”,否则随便，不传都行

    source = "dev"
    target = "prod"

    choose_action(source, target, url_ids, query_token, run_task_token, target_folder_name)

    # 原始一点，需要改多一些地方
    # for url_id in url_ids:
    #     print(f"\n{'=' * 50}")
    #     print(f"处理任务 (URL ID: {url_id})")
    #     print(f"{'=' * 50}")
    #     Query_url_dev = f"http://dc.dev.datastory.com.cn/application/market/job/v1/detail?id={url_id}"
    #     Query_url_prod = f"https://dc.datastory.com.cn/application/market/job/v1/detail?id={url_id}&uuu=banyan"
    #
    #     result = run_datamarket_job(url_id, sheet_id,
    #                                 Query_url=Query_url_dev, Query_token=query_token,
    #                                 run_task_url=run_task_url_prod, run_task_token=run_task_token)
