"""跨环境批量重载数据市场任务。

执行流程：
1. 根据 source 环境获取查询 token，并读取已有任务配置。
2. 根据 target 环境获取运行 token，并创建或复用目标文件夹。
3. 替换任务配置中的文件夹、导出方式、工作流和任务名称。
4. 调用 target 环境的任务运行接口，逐个重新创建任务。

dev 和 prod 的 token 不能跨环境使用。脚本因此分别获取 query_token 和
run_task_token，并将所有环境相关地址及固定参数集中放在 ENVIRONMENT_CONFIG
中管理。
"""

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Union

import requests


# 所有网络请求统一使用该超时时间，避免接口异常时脚本无限等待。
REQUEST_TIMEOUT = 30

# 接口默认将重载结果保存到本地；调用者可以传入其他配置覆盖该值。
DEFAULT_EXPORT_CONFIG = {"local": {}}

# 所有环境差异集中维护，防止认证地址、业务接口或固定参数互相串用。
# *_params 表示对应接口每次请求都必须携带的固定查询参数。
ENVIRONMENT_CONFIG = {
    "dev": {
        "auth_url": "http://dc.dev.datastory.com.cn/auth/obtain",
        "detail_url": "http://dc.dev.datastory.com.cn/application/market/job/v1/detail",
        "detail_params": {},
        "run_url": "http://dc.dev.datastory.com.cn/application/market/job/v1/run", # 测试 特点站点创建任务
        # "run_url":"http://dc.dev.datastory.com.cn/application/market/plugin/job/run?uuu=banyan", # 测试 自定义站点创建任务

        "sheet_add_url": "http://dc.dev.datastory.com.cn/sheet/add",
        "sheet_add_params": {},
        "sheet_list_url": "http://dc.dev.datastory.com.cn/sheet/list",
        "sheet_list_params": {"uuu": "banyan"},
    },
    "prod": {
        "auth_url": "https://dc.datastory.com.cn/auth/obtain",
        "detail_url": "https://dc.datastory.com.cn/application/market/job/v1/detail",
        "detail_params": {"uuu": "banyan"},
        "run_url": "https://dc.datastory.com.cn/application/market/job/v1/run", # 生产 特点站点创建任务
        # "run_url": "https://dc.datastory.com.cn/application/market/plugin/job/run", # 生产 自定义站点创建任务
        "sheet_add_url": "https://dc.datastory.com.cn/sheet/add",
        "sheet_add_params": {"uuu": "banyan"},
        "sheet_list_url": "https://dc.datastory.com.cn/sheet/list",
        "sheet_list_params": {"uuu": "banyan"},
    },
}

# API 中 ID 通常是整数，但保留字符串类型以兼容从文件读取的值。
JobId = Union[int, str]
SheetId = Union[int, str]


def _get_environment_config(environment: str) -> Dict[str, Any]:
    """获取指定环境的完整接口配置。

    参数:
        environment: 环境名称，目前仅支持 ``dev`` 和 ``prod``。

    返回:
        包含认证、任务和文件夹接口地址及固定参数的字典。

    异常:
        ValueError: environment 不受支持时抛出，防止请求被发往错误环境。
    """
    try:
        return ENVIRONMENT_CONFIG[environment]
    except KeyError as exc:
        valid_environments = ", ".join(ENVIRONMENT_CONFIG)
        raise ValueError(f"环境必须是以下值之一: {valid_environments}") from exc


def _endpoint_params(
    environment: str,
    config_key: str,
    **request_params: Any,
) -> Dict[str, Any]:
    """合并某个环境端点的固定参数与本次请求参数。

    参数:
        environment: 接口所属环境。
        config_key: ENVIRONMENT_CONFIG 中保存固定参数的键名。
        **request_params: 当前请求的动态参数，例如 jobId 或文件夹名称。

    返回:
        可直接传给 requests 的 params 字典。动态参数与固定参数重名时，
        动态参数优先。
    """
    config = _get_environment_config(environment)
    return {**config[config_key], **request_params}


def _authorization_headers(token: str) -> Dict[str, str]:
    """生成包含 JSON 内容类型和认证 token 的请求头。

    参数:
        token: 当前请求所属环境签发的认证 token。

    返回:
        可直接传给 requests 的 headers 字典。
    """
    return {
        "Content-Type": "application/json",
        "Authorization": token,
    }


def run_datamarket_job(
    url_id: JobId,
    sheet_id: SheetId,
    export_config: Optional[Mapping[str, Any]] = None,
    query_url: Optional[str] = None,
    query_token: Optional[str] = None,
    run_task_url: Optional[str] = None,
    run_task_token: Optional[str] = None,
    taskEnd: Optional[str] = "",
    query_params: Optional[Mapping[str, Any]] = None,
) -> Optional[str]:
    """读取源任务配置，并使用目标环境 token 创建新任务。

    为兼容原来的直接调用方式，``query_url`` 仍可包含完整查询参数；
    批量入口则通过 ``query_params`` 传递参数。

    参数:
        url_id: 源任务的 jobId，仅用于日志和定位失败任务。
        sheet_id: 目标环境中用于保存新任务的文件夹 ID。
        export_config: 新任务的导出配置；不传时使用本地保存配置。
        query_url: 源环境的任务详情接口地址。
        query_token: 源环境签发的 token，用于读取原任务。
        run_task_url: 目标环境的任务运行接口地址。
        run_task_token: 目标环境签发的 token，用于创建新任务。
        taskEnd: 添加到原任务名称末尾的后缀；传入 None 等同于空字符串。
        query_params: 任务详情接口的查询参数。

    返回:
        创建成功时返回运行接口的原始响应文本；任一步骤失败时返回 None。
    """
    if not all((query_url, query_token, run_task_url, run_task_token)):
        print("任务请求缺少URL或token，已跳过")
        return None

    # 第一步：使用源环境 token 获取原任务的完整配置。
    try:
        print(f"正在获取任务配置 (URL ID: {url_id})...")
        response = requests.get(
            query_url,
            headers=_authorization_headers(query_token),
            params=query_params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        response_data = response.json()
        print(f"任务配置获取成功，请求URL: {response.url}")
    except ValueError as exc:
        print(f"解析任务配置响应失败: {exc}")
        return None
    except requests.exceptions.RequestException as exc:
        print(f"获取任务配置失败: {exc}")
        return None

    # 第二步：校验业务响应，避免后续直接索引异常结构导致难以定位的问题。
    if not isinstance(response_data, dict):
        print("任务配置响应不是JSON对象")
        return None

    source_request_data = response_data.get("data")
    if source_request_data is None:
        print(
            "响应中的data字段为空，任务可能不存在或无权访问 "
            f"(URL ID: {url_id})"
        )
        return None
    if not isinstance(source_request_data, dict):
        print("响应中的data字段格式异常")
        return None

    # 第三步：复制原配置后覆盖目标环境相关字段，避免修改原响应对象。
    # workflowId 必须清空，否则新任务可能仍关联源环境中的工作流。
    new_request_data = source_request_data.copy()
    selected_export_config = (
        DEFAULT_EXPORT_CONFIG if export_config is None else export_config
    )
    new_request_data["exportConfig"] = dict(selected_export_config)
    new_request_data["sheetId"] = sheet_id
    new_request_data["workflowId"] = ""
    new_request_data["jobName"] = (
        f'{new_request_data.get("jobName", "")}{taskEnd or ""}'
    )

    # 第四步：使用目标环境 token 提交修改后的任务配置。
    try:
        response = requests.post(
            run_task_url,
            json=new_request_data,
            headers=_authorization_headers(run_task_token),
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        print(response.text)
        return response.text
    except requests.exceptions.RequestException as exc:
        print(f"创建任务失败: {exc}")
        return None


def get_token(
    username: str,
    password: str,
    url: Optional[str] = None,
    *,
    environment: str = "prod",
) -> Optional[str]:
    """从指定环境获取 token，失败时返回 ``None``。

    ``url`` 仅用于兼容原来传入自定义认证地址的调用；未传时必须根据
    ``environment`` 选择地址。

    参数:
        username: 登录用户名。
        password: 登录密码。
        url: 可选的自定义认证地址。一般无需传入。
        environment: 未指定 url 时用于选择认证地址的环境名称。

    返回:
        认证成功时返回 token 字符串；网络、解析或响应格式异常时返回 None。
    """
    # 显式 url 的优先级更高，用于保持旧调用方式和临时调试能力。
    auth_url = url or _get_environment_config(environment)["auth_url"]

    try:
        response = requests.post(
            auth_url,
            data={"username": username, "password": password},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        response_data = response.json()
    except ValueError as exc:
        print(f"解析token响应失败: {exc}")
        return None
    except requests.exceptions.RequestException as exc:
        print(f"获取token失败: {exc}")
        return None

    token = response_data.get("data") if isinstance(response_data, dict) else None
    if not isinstance(token, str) or not token:
        print(f"响应中没有找到token: {response.text}")
        return None
    return token


def load_accounts(
    filename: Optional[Union[str, Path]] = None,
) -> Dict[str, Dict[str, str]]:
    """从 JSON 文件加载账号配置。

    参数:
        filename: 账号文件路径。未传时读取当前脚本同目录的 accounts.json。

    返回:
        以账号别名为键、账号信息为值的字典；读取或格式校验失败时返回
        空字典。
    """
    # 使用脚本同目录作为默认位置，避免启动目录改变后找不到账号文件。
    account_file = (
        Path(filename) if filename else Path(__file__).with_name("accounts.json")
    )

    try:
        with account_file.open("r", encoding="utf-8") as file:
            accounts = json.load(file)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"读取账号文件失败: {exc}")
        return {}

    if not isinstance(accounts, dict):
        print(f"账号文件必须是JSON对象: {account_file}")
        return {}

    print(f"从 {account_file} 加载了 {len(accounts)} 个账号")
    return accounts


def get_token_by_name(
    account_name: str,
    accounts: Mapping[str, Mapping[str, str]],
    environment: str = "prod",
) -> Optional[str]:
    """使用账号别名从指定环境获取 token。

    参数:
        account_name: accounts.json 中配置的账号别名。
        accounts: ``load_accounts`` 返回的账号配置。
        environment: 需要登录的环境。查询任务传 source，创建任务传 target。

    返回:
        获取成功时返回 token；账号不存在、字段缺失或认证失败时返回 None。

    异常:
        ValueError: environment 不受支持时由环境校验函数抛出。
    """
    # 先校验环境，避免把环境拼写错误误判为账号问题。
    _get_environment_config(environment)

    account_info = accounts.get(account_name)
    if not isinstance(account_info, Mapping):
        print(f"错误: 未找到账号 '{account_name}'")
        return None

    username = account_info.get("username")
    password = account_info.get("password")
    if not username or not password:
        print(f"错误: 账号 '{account_name}' 缺少username或password")
        return None

    print(f"正在为 '{account_name}' 获取 {environment} 环境token...")
    return get_token(username, password, environment=environment)


def _normalize_folder_environment(folder_path: str) -> str:
    """将文件夹接口的旧环境参数转换为标准环境名称。

    参数:
        folder_path: ``dev``、``prod``，或旧调用中代表 prod 的空字符串。

    返回:
        标准化后的 ``dev`` 或 ``prod``。

    异常:
        ValueError: 标准化后的环境名称不受支持时抛出。
    """
    environment = "prod" if folder_path == "" else folder_path
    _get_environment_config(environment)
    return environment


def create_new_folder(
    folder_name: str,
    folder_token: str,
    folder_path: str,
) -> Optional[SheetId]:
    """在目标环境中创建用于保存新任务的文件夹。

    参数:
        folder_name: 目标文件夹名称。
        folder_token: 目标环境签发的 token。
        folder_path: 目标环境名称；保留该参数名以兼容旧调用。

    返回:
        创建成功或找到同名文件夹时返回 sheetId，否则返回 None。
    """
    environment = _normalize_folder_environment(folder_path)
    config = _get_environment_config(environment)

    print(f"正在 {environment} 环境创建文件夹")
    try:
        response = requests.post(
            config["sheet_add_url"],
            headers=_authorization_headers(folder_token),
            params=_endpoint_params(
                environment,
                "sheet_add_params",
                name=folder_name,
            ),
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        response_data = response.json()
    except ValueError as exc:
        print(f"解析创建文件夹响应失败: {exc}")
        return None
    except requests.exceptions.RequestException as exc:
        print(f"创建文件夹失败: {exc}")
        return None

    # 创建接口成功时，data 字段就是后续运行任务需要的 sheetId。
    if not isinstance(response_data, dict):
        print("创建文件夹响应格式异常")
        return None

    if response_data.get("success"):
        sheet_id = response_data.get("data")
        if sheet_id is None:
            print("创建成功，但响应中没有sheetId")
            return None
        print("sheetId:", sheet_id)
        return sheet_id

    # 旧接口在文件夹重名时返回success=false，因此继续查询已有文件夹。
    print("文件夹未创建，开始查询是否存在同名文件夹")
    return query_folder_id(folder_token, folder_name, environment)


def query_folder_id(
    run_task_token: str,
    target_name: str,
    folder_path: str,
) -> Optional[SheetId]:
    """根据文件夹名称查询指定环境中的 sheetId。

    参数:
        run_task_token: 目标环境签发的 token。
        target_name: 需要查找的文件夹名称。
        folder_path: 目标环境名称；空字符串兼容旧版的 prod 写法。

    返回:
        找到同名文件夹时返回其 ID，否则返回 None。
    """
    environment = _normalize_folder_environment(folder_path)
    config = _get_environment_config(environment)

    try:
        response = requests.get(
            config["sheet_list_url"],
            headers=_authorization_headers(run_task_token),
            params=_endpoint_params(environment, "sheet_list_params"),
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        response_data = response.json()
    except ValueError as exc:
        print(f"解析文件夹列表响应失败: {exc}")
        return None
    except requests.exceptions.RequestException as exc:
        print(f"查询文件夹失败: {exc}")
        return None

    if not isinstance(response_data, dict) or not response_data.get("success"):
        message = response_data.get("message") if isinstance(response_data, dict) else None
        print("接口返回失败或数据格式异常:", message)
        return None

    folder_list = response_data.get("data")
    if not isinstance(folder_list, list):
        print("文件夹列表中的data字段格式异常")
        return None

    # 接口没有按名称过滤的参数，因此在完整列表中精确匹配文件夹名称。
    for item in folder_list:
        if isinstance(item, dict) and item.get("name") == target_name:
            found_id = item.get("id")
            if found_id is not None:
                print(f'文件夹名称 "{target_name}" 对应的ID是: {found_id}')
                return found_id

    print(f'未找到名称为 "{target_name}" 的文件夹。')
    return None


def choose_action(
    source: str,
    target: str,
    url_ids: Iterable[JobId],
    query_token: str,
    run_task_token: str,
    target_folder_name: str,
    taskEnd: Optional[str] = "",
) -> List[Tuple[JobId, Optional[str]]]:
    """按照源环境和目标环境批量重建任务。

    参数:
        source: 读取原任务的环境。
        target: 创建新任务和目标文件夹的环境。
        url_ids: 需要重载的一个或多个 jobId。
        query_token: source 环境签发的查询 token。
        run_task_token: target 环境签发的运行 token。
        target_folder_name: target 环境中用于保存任务的文件夹名称。
        taskEnd: 追加到每个原任务名称后的统一后缀。

    返回:
        ``(jobId, 响应文本)`` 列表。单个任务失败时响应文本为 None；
        无法获得目标文件夹 ID 时返回空列表并停止整批任务。

    异常:
        ValueError: 环境不受支持，或任一 token 为空时抛出。
    """
    # 在产生任何写操作前先校验两个环境及 token。
    source_config = _get_environment_config(source)
    target_config = _get_environment_config(target)
    if not query_token or not run_task_token:
        raise ValueError("query_token和run_task_token不能为空")

    # 所有新任务共用同一个目标文件夹，只需在循环前创建或查询一次。
    print(f"正在运行 {source} to {target}")
    sheet_id = create_new_folder(target_folder_name, run_task_token, target)
    if sheet_id is None:
        print("无法获取目标文件夹ID，批量任务已终止")
        return []

    # 单个任务失败不会阻断后续任务，并在 results 中以 None 标记失败。
    results: List[Tuple[JobId, Optional[str]]] = []
    for url_id in url_ids:
        print(f"\n{'=' * 50}")
        print(f"处理任务 (URL ID: {url_id})")
        print(f"{'=' * 50}")

        result = run_datamarket_job(
            url_id,
            sheet_id,
            query_url=source_config["detail_url"],
            query_token=query_token,
            run_task_url=target_config["run_url"],
            run_task_token=run_task_token,
            taskEnd=taskEnd,
            query_params=_endpoint_params(source, "detail_params", id=url_id),
        )
        results.append((url_id, result))

    return results


if __name__ == "__main__":
    # ------------------------- 可修改的运行配置 -------------------------
    # source 是原任务所在环境，target 是新任务需要创建到的环境。
    source = "prod"
    target = "prod"

    # 需要重载的任务 ID，可在列表中一次填写多个。
    # url_ids = [20085524,19700213,19913715,19840397,19840398,20091933,20121685,20210120,20196315,20091805,20196312,20200600,20196330,]
    # url_ids = [20756774,20756760,20756747,20756734,20756730,20756728,20756720,20756711,20756683,20756673,20756015] # 鹰角11个自定义站点测试
    url_ids = [21158207] # 数皆0806新增小红书用户url

    # 新任务共用该文件夹；重名时会自动查询并复用已有文件夹。
    target_folder_name = "微信视频号和公众号回溯"

    # 同一个任务多次重载时用后缀区分；不需要后缀时设置为空字符串。
    task_end = "-重试"  # 同一个任务多次重载时，用后缀区分任务名称。
    # task_end = ""

    # 账号别名来自 accounts.json，source 和 target 可以使用不同账号。
    query_account_name = "admin账号"
    run_task_account_name = "admin账号"
    # ------------------------------------------------------------------

    accounts = load_accounts()

    # 查询 token 必须由 source 签发，运行 token 必须由 target 签发。
    query_token = get_token_by_name(query_account_name, accounts, source)
    run_task_token = get_token_by_name(run_task_account_name, accounts, target)

    # 任一 token 获取失败都立即结束，避免继续调用文件夹和任务接口。
    if not query_token or not run_task_token:
        raise SystemExit("token获取失败，任务未执行")

    # 所有配置和认证均准备完成后，开始执行批量重载。
    choose_action(
        source,
        target,
        url_ids,
        query_token,
        run_task_token,
        target_folder_name,
        task_end,
    )
