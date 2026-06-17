import requests
import json


def generate_query_code(config_json):
    """
    根据JSON配置生成对应的API查询代码

    :param config_json: 包含查询配置的JSON字符串
    :return: 生成的Python代码字符串
    """
    # 解析JSON配置
    config = json.loads(config_json)

    # 构建代码模板
    code_template = f"""import requests
import json

url = "https://dc.datastory.com.cn/banyan/searchInBanyan"

# ===== 注意：Authorization和Cookie会过期，请定期更新 =====
headers = {{
  'Content-Type': 'application/json',
  'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJrb3lAZGF0YXN0b3J5LmNvbS5jbiIsImF1ZGllbmNlIjoid2ViIiwiY3JlYXRlZCI6MTc2NTUzMjg1NjU5OSwicHciOiJBaXIxNjA2MzAiLCJleHAiOjE3NjYxMzc2NTZ9.dkZQUdPjAvN0w-XsyN-ZizGHox69SkaI_3tfbzH1WbKRPvxzSRFQvTUbQxrMHkjAFLi4oOMjwyIiOM1ih1wiGA',
  'Cookie': 'dc-login-iden=.datastory.com.cn#e3279c4f-42cd-4195-9410-15efa172e134; SESSION=4aa8a18b-f80a-4fa4-b4e6-026514bdcea3'
}}

# 动态生成的查询配置
payload = {json.dumps(config, indent=4, ensure_ascii=False)}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.text)

"""

    return code_template


# 使用示例
if __name__ == "__main__":
    # 您提供的新配置数据
    new_config = """{
        "dataType":"NewsForum",
        "banyanType":"elf",
        "searchType":"Post",
        "searchCondition":[
            {
                "fieldName":"site_name",
                "operation":"mp",
                "fieldValue":["懂车帝",""]
            },
            {
                "fieldName":"publish_timestamp",
                "operation":"ltegte",
                "fieldValue":[1768233600000,1770911999999]
            }
        ],
        "timeRange":"1768233600000,1770911999999",
        "needReturnFields":"user_item_id,cat_id",
        "sortCondition":{
            "sortFieldName":"publish_timestamp",
            "order":"desc"
        }
    }"""

    # 生成代码
    generated_code = generate_query_code(new_config)

    # 保存到文件
    output_file = "dynamic_query.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(generated_code)

    print(f"✅ 代码已生成并保存至: {output_file}")
    print("\n⚠️ 重要提示:")
    print("1. 生成的代码包含有效期的认证信息，请勿提交到公共代码仓库")
    print("2. 首次运行前请更新headers中的Authorization和Cookie值")
    print("3. 运行命令: python dynamic_query.py")