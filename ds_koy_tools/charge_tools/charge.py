"""
用户充值接口 - 调用 /admin/user/charge/update 进行充值操作

使用方式:
    1. 修改下方 CHARGE_DATA 列表中的充值数据
    2. 运行脚本即可完成充值
"""

import json
import os
import requests
from typing import Optional, List, Dict, Any


# ============ 配置区域 ============

# 认证信息（使用 admin 账号才有充值权限）
AUTH_URL = "https://dc.datastory.com.cn/auth/obtain"
USERNAME = "hermes_admin@datastory.com.cn"
PASSWORD = "hSm8W2MmuHy?J@!NzM2T"

# 充值接口
CHARGE_URL = "https://dc.datastory.com.cn/admin/user/charge/update?uuu=banyan"

# 用户列表缓存文件（由 query_userList.py 生成）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_LIST_FILE = os.path.join(SCRIPT_DIR, "user_list.json")


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


def find_uid_by_email(email: str) -> Optional[int]:
    """
    从本地 user_list.json 文件中根据邮箱匹配 uid（纯本地，无需网络）。

    :param email: 用户邮箱
    :return: 用户 uid，未找到返回 None
    """
    if not os.path.exists(USER_LIST_FILE):
        print(f"❌ 用户列表文件不存在: {USER_LIST_FILE}")
        print("   请先运行 query_userList.py 生成该文件")
        return None

    with open(USER_LIST_FILE, "r", encoding="utf-8") as f:
        user_map = json.load(f)

    uid = user_map.get(email)
    if uid is not None:
        print(f"✅ 邮箱 {email} → uid={uid}")
        return uid
    else:
        print(f"⚠️ 未找到邮箱为 {email} 的用户")
        return None


def resolve_charge_data(charge_data: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
    """
    将 CHARGE_DATA 中的 email 字段解析为 uid。

    :param charge_data: 包含 email 字段的充值数据列表
    :return: 解析后的充值数据列表（含 uid），失败返回 None
    """
    resolved = []
    for item in charge_data:
        email = item.get("email")
        uid = item.get("uid")

        if uid is not None:
            # 已有 uid，直接使用
            resolved.append(item)
        elif email:
            # 通过邮箱查 uid
            found_uid = find_uid_by_email(email)
            if found_uid is None:
                print(f"❌ 无法解析邮箱 {email} 对应的 uid，跳过该条")
                return None
            new_item = {k: v for k, v in item.items() if k != "email"}
            new_item["uid"] = found_uid
            resolved.append(new_item)
        else:
            print(f"❌ 充值数据缺少 email 和 uid 字段，跳过: {item}")
            return None

    return resolved


def post_charge(token: str, charge_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    发送充值请求。

    :param token: 认证 Token
    :param charge_data: 充值数据列表
    :return: 接口返回的 JSON 数据，失败返回 None
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
    }

    try:
        print(f"\n正在发送充值请求...")
        print(f"请求 URL: {CHARGE_URL}")
        # 使用 json 参数自动处理编码，requests 会用 json.dumps() 序列化
        response = requests.post(
            CHARGE_URL,
            json=charge_data,  # 直接用 json 参数，省去手动 json.dumps
            headers=headers,
            timeout=30
        )
        print(f"HTTP 状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        print("充值请求超时")
        return None
    except requests.RequestException as e:
        print(f"充值请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"服务端响应: {e.response.text}")
        return None
    except json.JSONDecodeError:
        # 响应可能不是 JSON
        print(f"响应非 JSON 格式: {response.text}")
        return None


def do_charge(charge_data: List[Dict[str, Any]]):
    """
    执行完整的充值流程：获取 Token -> 解析邮箱为 uid -> 发送充值请求。

    :param charge_data: 充值数据列表（可含 email 字段，会自动解析为 uid）
    """
    print("=" * 50)
    print("用户充值脚本")
    print("=" * 50)

    # 1. 获取 Token
    token = get_token(USERNAME, PASSWORD)
    if not token:
        print("\n❌ 充值失败：无法获取 Token")
        return

    # 2. 解析 email → uid（从本地 user_list.json）
    resolved_data = resolve_charge_data(charge_data)
    if resolved_data is None:
        print("\n❌ 充值失败：无法解析用户 email 到 uid")
        return

    # 3. 打印待充值信息
    print(f"\n待充值 {len(resolved_data)} 条记录：")
    for i, item in enumerate(resolved_data, 1):
        print(f"  {i}. uid={item['uid']}, number={item['number']}, "
              f"dataType={item['dataType']}, function={item['function']}, "
              f"chargeType={item['chargeType']}, remark={item.get('remark')}")

    # 4. 发送充值请求
    result = post_charge(token, resolved_data)

    # 5. 结果处理
    if result is not None:
        print(f"\n✅ 充值请求完成，返回数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        print("\n❌ 充值失败，请检查上方日志排查原因")


# ============ 入口 ============

if __name__ == "__main__":
    # ============ 充值配置 ============
    # dataType:  默认 1
    # function:  数据类型
    #   F类数据 -> 11 ;  G类数据 -> 12 ;  A类数据 -> 2 ;  数据看板 -> 13 ;     智能洞察 -> 14 ;
    #   D类数据 -> 5  ;  E类数据 -> 10 ;  C类数据 -> 4 ;  社媒API调用量 -> 9 ; 分析报告 -> analyse_type ;
    #   B类数据 -> 3  ;  H类数据 -> 15 ;
    # chargeType: 充值类型 1=充值；2=扣费
    # number:    充值数量
    # email:     用户邮箱（会自动从 user_list.json 解析为 uid）
    # remark:    备注（可为 null）

    CHARGE_DATA: List[Dict[str, Any]] = [
        {
            "dataType": 1,
            "function": "15",
            "chargeType": 1,
            "number": 20000000,
            "email": "koy@datastory.com.cn",
            "remark": None
        },
        # 批量充值，可继续添加：
        # {
        #     "dataType": 1,
        #     "function": "4",
        #     "chargeType": 1,
        #     "number": 50000,
        #     "email": "xxx@example.com",
        #     "remark": "测试充值"
        # },
    ]

    do_charge(CHARGE_DATA)

    # http: // dc.dev.datastory.com.cn / admin / user / charge / update
    # uid=309
