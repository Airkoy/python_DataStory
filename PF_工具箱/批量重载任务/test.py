email_list = ["jingyi.xue@bluefocus.com", "yongjian.liu@bluefocus.com"]

for email in email_list:
    query_url = f"https://dc.datastory.com.cn/user/transaction/api?uuu=banyan&startTime=1772294400000&endTime=1774540799000&keyword={email}&interfaceName=&page=1&size=10000"
    print(f'query_url = "{query_url}"')

query_url = "https://dc.datastory.com.cn/user/transaction/api?uuu=banyan&startTime=1772294400000&endTime=1774540799000&keyword=xinhua.zhang1@bluefocus.com&interfaceName=&page=1&size=10000"
