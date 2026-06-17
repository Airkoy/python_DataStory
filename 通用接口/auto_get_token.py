import json
import time
from pathlib import Path
from typing import Optional, Dict, Any

import requests


class TokenManager:
    """
    用于获取和管理认证 Token 的类。

    该类封装了从文件中读取账号信息、请求新 Token、以及缓存 Token 的逻辑，
    避免在 Token 有效期内重复请求，提高了效率和健壮性。

    使用示例:
        try:
            manager = TokenManager()
            account_name = "your_account_name"
            headers = manager.get_headers(account_name)
            if headers:
                print(f"✅ 成功获取 '{account_name}' 的请求头: {headers}")
                # response = requests.get("some_api_endpoint", headers=headers)
                # print(response.json())
        except (AccountError, TokenError) as e:
            print(f"❌ 操作失败: {e}")

    """
    # 获取脚本文件所在目录
    _BASE_DIR = Path(__file__).parent
    DEFAULT_ACCOUNTS_FILE = _BASE_DIR / "accounts.json"
    DEFAULT_CACHE_FILE = _BASE_DIR / "token_cache.json"
    DEFAULT_AUTH_URL = "https://dc.datastory.com.cn/auth/obtain"
    # Token 有效期，单位为秒（例如：3600 = 1小时）
    TOKEN_EXPIRATION = 3600

    def __init__(self, accounts_file: Path = DEFAULT_ACCOUNTS_FILE, cache_file: Path = DEFAULT_CACHE_FILE):
        """
        初始化 TokenManager。

        :param accounts_file: 存储账号凭据的 JSON 文件路径。
        :param cache_file: 用于缓存 Token 的 JSON 文件路径。
        """
        self.accounts_file = accounts_file
        self.cache_file = cache_file
        self.accounts = self._load_accounts()
        self.token_cache = self._load_cache()

    def _load_accounts(self) -> Dict[str, Any]:
        """从文件加载账号信息。"""
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise AccountError(f"账号文件未找到: {self.accounts_file}")
        except json.JSONDecodeError:
            raise AccountError(f"无法解析账号文件: {self.accounts_file}")

    def _load_cache(self) -> Dict[str, Any]:
        """从文件加载缓存的 Token。"""
        if not self.cache_file.exists():
            return {}
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_cache(self):
        """将 Token 缓存保存到文件。"""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.token_cache, f, indent=4)

    def _get_cached_token(self, account_name: str) -> Optional[str]:
        """
        尝试从缓存中获取有效的 Token。

        :param account_name: 账号名称。
        :return: 如果存在且未过期，则返回 Token，否则返回 None。
        """
        cache_entry = self.token_cache.get(account_name)
        if cache_entry and time.time() < cache_entry.get("expires_at", 0):
            return cache_entry.get("token")
        return None

    def _fetch_new_token(self, username: str, password: str) -> str:
        """
        请求新的 Token。

        :param username: 用户名。
        :param password: 密码。
        :return: 新获取的 Token。
        :raises TokenError: 如果请求失败或返回数据格式不正确。
        """
        try:
            response = requests.post(self.DEFAULT_AUTH_URL, data={"username": username, "password": password}, timeout=10)
            response.raise_for_status()
            data = response.json()
            token = data.get("data")
            if not token or not isinstance(token, str):
                raise TokenError("获取 Token 失败：返回的数据格式不正确。")
            return token
        except requests.Timeout:
            raise TokenError("获取 Token 超时。")
        except requests.RequestException as e:
            raise TokenError(f"获取 Token 网络请求失败: {e}")

    def get_token(self, account_name: str) -> str:
        """
        获取指定账号的 Token，优先从缓存读取。

        :param account_name: 账号名称。
        :return: 获取到的 Token。
        :raises AccountError: 如果账号不存在。
        :raises TokenError: 如果获取 Token 失败。
        """
        # 1. 尝试从缓存获取
        cached_token = self._get_cached_token(account_name)
        if cached_token:
            print(f"🔑 从缓存中成功获取 '{account_name}' 的 Token。")
            return cached_token

        # 2. 缓存未命中或已过期，则请求新 Token
        print(f"🔄 缓存未命中或已过期，正在为 '{account_name}' 请求新 Token...")
        account_info = self.accounts.get(account_name)
        if not account_info:
            raise AccountError(f"账号 '{account_name}' 不存在于 {self.accounts_file}")

        username = account_info.get("username")
        password = account_info.get("password")
        if not username or not password:
            raise AccountError(f"账号 '{account_name}' 的凭据不完整。")

        new_token = self._fetch_new_token(username, password)

        # 3. 更新缓存
        self.token_cache[account_name] = {
            "token": new_token,
            "expires_at": time.time() + self.TOKEN_EXPIRATION
        }
        self._save_cache()
        print(f"✅ 成功获取并缓存 '{account_name}' 的新 Token。")
        return new_token

    def get_headers(self, account_name: str) -> Dict[str, str]:
        """
        获取包含认证 Token 的请求头。

        :param account_name: 账号名称。
        :return: 包含 'Authorization' 和 'Content-Type' 的字典。
        """
        token = self.get_token(account_name)
        headers = {
            "Content-Type": 'application/json',
            'Authorization': token,
        }
        return headers


class AccountError(Exception):
    """与账号相关的错误。"""
    pass


class TokenError(Exception):
    """与 Token 获取相关的错误。"""
    pass


# --- 使用示例 ---
if __name__ == "__main__":
    try:
        # 初始化管理器
        token_manager = TokenManager()

        # 指定要使用的账号名称
        # 请确保 "admin账号" 在您的 "accounts.json" 文件中存在
        target_account = "admin账号"

        # 获取 Token
        token = token_manager.get_token(target_account)
        print(token)
        print()

        # 获取请求头
        headers = token_manager.get_headers(target_account)
        print("headers = " + json.dumps(headers, indent=2, ensure_ascii=False))

    except (AccountError, TokenError) as e:
        print(f"\n❌ 操作失败: {e}")
    except Exception as e:
        print(f"\n❌ 发生未知错误: {e}")
