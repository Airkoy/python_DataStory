"""
用户列表查询接口 - 调用 /admin/user/list 获取所有用户信息

基于以下请求信息生成:
    GET https://dc.datastory.com.cn/admin/user/list?page=0&size=1000000&uuu=banyan

功能:
    query_user_list()   - 获取全部用户列表，同时更新当前缓存和每日快照
    find_uid_by_email() - 从当前缓存中根据邮箱匹配 uid（纯本地，无需网络）

使用方式:
    python query_userList.py
"""

import json
from datetime import datetime
from pathlib import Path

import requests
from typing import Optional, Dict, Any


# ============ 配置区域 ============

# 认证信息（使用 admin 账号才有权限）
AUTH_URL = "https://dc.datastory.com.cn/auth/obtain"
USERNAME = "hermes_admin@datastory.com.cn"
PASSWORD = "hSm8W2MmuHy?J@!NzM2T"

# 用户列表查询接口
USER_LIST_URL = "https://dc.datastory.com.cn/admin/user/list"

# user_list.json 是下游统一读取的当前缓存；带日期文件用于保留每日快照。
SCRIPT_DIR = Path(__file__).resolve().parent
USER_LIST_FILE = SCRIPT_DIR / "user_list.json"

# 查询参数
QUERY_PARAMS = {
    "page": 0,
    "size": 1000000,
    "uuu": "banyan",
}


# ============ 核心函数 ============

def get_token(username: str, password: str) -> Optional[str]:
    """
    获取认证 Token。

    :param username: 用户名
    :param password: 密码
    :return: Token 字符串，失败返回 None
    """
    try:
        print(f"正在获取 Token (账号: {username})...")
        response = requests.post(
            AUTH_URL,
            data={"username": username, "password": password},
            timeout=10
        )
        response.raise_for_status()
        token = response.json().get("data")
        if not token:
            print(f"获取 Token 失败：响应中无 data 字段，原始响应: {response.text}")
            return None
        print("Token 获取成功")
        return token
    except requests.Timeout:
        print("获取 Token 超时")
        return None
    except requests.RequestException as e:
        print(f"获取 Token 网络请求失败: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"解析 Token 响应失败: {e}")
        return None


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    """原子写入 JSON，避免中途中断留下不完整缓存。"""
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    temporary_path.replace(path)


def save_user_cache(user_map: Dict[str, int]) -> tuple[Path, Path]:
    """更新稳定缓存、每日快照及其生成信息。"""
    generated_at = datetime.now().astimezone()
    snapshot_file = SCRIPT_DIR / f"user_list_{generated_at:%Y%m%d}.json"
    metadata = {
        "generated_at": generated_at.isoformat(timespec="seconds"),
        "source": USER_LIST_URL,
        "user_count": len(user_map),
    }

    for cache_file in (USER_LIST_FILE, snapshot_file):
        _write_json(cache_file, user_map)
        _write_json(cache_file.with_suffix(".meta.json"), metadata)

    return USER_LIST_FILE, snapshot_file


def query_user_list(token: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    """
    获取全部用户列表，提取 email/uid 并更新当前缓存和每日快照。

    :param token:  admin 账号的认证 Token
    :param params: 查询参数字典
    :return: 接口返回的 JSON 数据，失败返回 None
    """
    if params is None:
        params = QUERY_PARAMS

    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
    }

    try:
        print(f"\n正在查询用户列表...")
        print(f"请求 URL: {USER_LIST_URL}")
        print(f"查询参数: {params}")
        response = requests.get(
            USER_LIST_URL,
            params=params,
            headers=headers,
            timeout=30
        )
        print(f"HTTP 状态码: {response.status_code}")

        response.raise_for_status()
        result = response.json()

        # 提取 email -> uid 映射
        data = result.get("data", {})
        users = data.get("content", []) or data.get("list", []) or []

        user_map = {}
        for user in users:
            email = user.get("email") or user.get("username") or ""
            uid = user.get("id") or user.get("uid", "")
            if email and uid:
                user_map[str(email)] = int(uid)

        current_file, snapshot_file = save_user_cache(user_map)
        print(f"✅ 当前用户缓存已更新: {current_file}")
        print(f"✅ 每日快照已保存: {snapshot_file}，共 {len(user_map)} 个用户")

        return result
    except requests.Timeout:
        print("查询用户列表超时")
        return None
    except requests.RequestException as e:
        print(f"查询用户列表请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"服务端响应: {e.response.text}")
        return None
    except json.JSONDecodeError:
        print(f"响应非 JSON 格式: {response.text[:200]}")
        return None


def find_uid_by_email(email: str, user_list_file: Path = USER_LIST_FILE) -> Optional[int]:
    """
    从本地用户缓存中根据邮箱匹配 uid（纯本地，无需网络）。

    :param email: 用户邮箱
    :return: 用户 uid，未找到返回 None
    """
    if not user_list_file.exists():
        print(f"❌ 用户列表文件不存在: {user_list_file}")
        print("   请先运行 query_user_list() 生成该文件")
        return None

    with user_list_file.open("r", encoding="utf-8") as f:
        user_map = json.load(f)

    uid = user_map.get(email)
    if uid is not None:
        print(f"✅ 找到用户: {email}, uid={uid}")
        return uid
    else:
        print(f"⚠️ 未找到邮箱为 {email} 的用户")
        return None


def do_query():
    """
    执行完整的查询流程：获取 Token -> 查询用户列表 -> 保存到 JSON。
    """
    print("=" * 50)
    print("用户列表查询")
    print("=" * 50)

    # 1. 获取 Token
    token = get_token(USERNAME, PASSWORD)
    if not token:
        print("\n❌ 查询失败：无法获取 Token")
        return

    # 2. 查询用户列表（同时更新 user_list.json 和每日快照）
    result = query_user_list(token)

    if result is not None:
        data = result.get("data", {})
        users = data.get("content", []) or data.get("list", []) or []
        print(f"\n共获取 {len(users)} 个用户")
        print(f"当前缓存路径: {USER_LIST_FILE}")
    else:
        print("\n❌ 查询失败，请检查上方日志排查原因")


# ============ 入口 ============

if __name__ == "__main__":
    do_query() # 运行后获取一次用户列表
    uid = find_uid_by_email("")

    # 从本地 JSON 文件根据邮箱查 uid
    # uid = find_uid_by_email("koy@datastory.com.cn")
    # print(f"uid = {uid}")
