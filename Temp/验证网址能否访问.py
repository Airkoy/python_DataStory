import requests
from requests.exceptions import RequestException, ConnectTimeout, SSLError
import time

# 要验证的所有 YouTube 网址
urls = [
    "https://www.youtube.com/@tencentvideo?si=-4GnNeaL2bSPFmaf",
    "https://www.youtube.com/@tencentvideominidrama?si=qEAY1zv4G9SdUEnO",
    "https://www.youtube.com/@tencentvideodrama?si=CktXpv4sAlaH3vzb",
    "https://www.youtube.com/@tencentvideosuspense?si=yc1-dJhBDSXujgWi",
    "https://www.youtube.com/@tencentvideoromantic?si=q16okrfIswrzLfTW",
    "https://www.youtube.com/@tencentvideocostume?si=FkCbEaPbPaqthyL7",
    "https://www.youtube.com/@wetvvietnam?si=0n_BDg4Llhi-uLTc",
    "https://www.youtube.com/@wetvtaiwanofficial?si=as7R7jkTrzLqMxEu",
    "https://www.youtube.com/@tencentvideoartist?si=SuzeQ8DTrGjXmP-H",
    "https://www.youtube.com/@tencentvideoanimation?si=gyheDIHPWKZ_6ELx",
    "https://www.youtube.com/@wetvcomedyofficial?si=2gxP1ylBTK0k7Fpl",
    "https://www.youtube.com/@tencentvideodocumentary?si=Rfxf0unv6jNLnW4N",
    "https://www.youtube.com/@tencentvideomovie?si=dOVIP2J3dquIfCKp",
    "https://www.youtube.com/@tencentvideoost?si=F1aHFSQ1-weDlQl4",
    "https://www.youtube.com/@chuangasia?si=Fa9H_GCV74ECCZ3X",
    "https://www.youtube.com/@wetvindonesia?si=JWSS9d7stZJTXIlg",
    "https://www.youtube.com/@wetvthailand?si=AevCU32vXSiJe6QQ",
    "https://www.youtube.com/@wetvenglish?si=x158q88wtdM1ojbl",
    "https://www.youtube.com/@wetvspanish?si=PiCYcm6liD1k5aSD",
    "https://www.youtube.com/@wetvarabic?si=NpsSl7P-10Cnf7yx",
    "https://www.youtube.com/@wetvturkish?si=EUOWKNzuiZvb1Vcd",
    "https://www.youtube.com/@wetvkorea?si=DQ4uTnbEjhGCtIpZ",
    "https://www.youtube.com/@wetvrussian?si=uHseh3rKFog_oXYR",
    "https://www.youtube.com/@wetvportuguese?si=rts022EN6awZAhOi",
    "https://www.youtube.com/@wetvmalaysia?si=B40txo6Mf1LDzsA5",
    "https://www.youtube.com/@wetvduniadrama?si=nsDYXCAfwa3nBm7Z",
    "https://www.youtube.com/@wetvthailand2?si=a6rIYeQlh_nisUcQ",
    "https://www.youtube.com/@wetvportugueseanimation?si=KfQqnZdKEOXlCgDI",
    "https://www.youtube.com/@tencentvideoshow?si=uFti_WTXoZ57rJx1",
    "https://www.youtube.com/@heartsignalofficialchannel?si=U8Dh5QHRUULYFijy",
    "https://www.youtube.com/channel/UCKYFMJiSiazXGNfulDOawXQ?si=EIanmAvfp6AugfFd",
    "https://www.youtube.com/@anexcitingoffer?si=xEbvuRRnExjR8p9a",
    "https://www.youtube.com/@wetv-hotshow?si=14mndJ8W4sKNKmLu",
    "https://www.youtube.com/@wonderlandofficialchannel?si=J8YXeitUY5MokFxz",
    "https://www.youtube.com/@wetv-classicvariety?si=6Z_dI88AH3sSkXvB",
    "https://www.youtube.com/channel/UCsbos5DhRZ7TZPr0hCutkoA?si=fSFBqIw7w0MXCp1y",
    "https://www.youtube.com/@thetruthofficialchannel?si=ICwXWul96q-HoIaq",
    "https://www.youtube.com/@wetvmovie?si=j5u4jg-iTTruIFH1",
    "https://www.youtube.com/@wetvoriginals?si=nwJ4_5Q3sqDMEs8K",
    "https://www.youtube.com/@wetvphilippines?si=0BNwgIIDrY0ih-E6",
    "https://www.youtube.com/@wetvjapan5543?si=62h7pPUVe2NdOmtF",
    "https://www.youtube.com/@wetvhindi7196?si=WqERgX79-xFuCMOi",
    "https://www.youtube.com/channel/UCU7LczbI2NTX4-DtAtkP-dA?si=lftgoB1OahURRJxc",
    "https://www.youtube.com/@youku-official?si=EGnQssC_P7_1yOAp",
    "https://www.youtube.com/@youkumovie?si=MW5CMMHvKcIgE7KP",
    "https://www.youtube.com/@youkushow?si=UO6KbkGEpKYu76QY",
    "https://www.youtube.com/@youkuanimation?si=KG6MkqdoPqL9A6zJ",
    "https://www.youtube.com/@youkudocumentary?si=hfDRI-x_PqkGr5ra",
    "https://www.youtube.com/@youkuenglishanimation-en?si=13di_hofYUe1EF9g",
    "https://www.youtube.com/@youkukids?si=jyh6BEtltqQwlvoe",
    "https://www.youtube.com/channel/UCLv530sGwXYiF1BZ7abwI0g?si=Kb4N-9MWfpkzKVWl",
    "https://www.youtube.com/@youkumonstermovie?si=1yxhSpCS0fghZMBL",
    "https://www.youtube.com/@youkuanimefanzhong?si=HJgGlJXR0uPx6iGz",
    "https://www.youtube.com/@youkuromance?si=y1RgVHJr7DTwWYyW",
    "https://www.youtube.com/channel/UCSRzkWQQaKM6jyJQ7WijC-A?si=9PV1iEVzZGWP0Ccy",
    "https://www.youtube.com/@youkukorea?si=9huJuWq6heD_o0eH",
    "https://www.youtube.com/@youkususpense?si=A1zjDpmZEG015o5X",
    "https://www.youtube.com/@youkuspanishmovie?si=NMyzA4JEYGYWOFa6",
    "https://www.youtube.com/@youkucostume?si=5fhCpmMdbeJRsouU",
    "https://www.youtube.com/@youkuhuayu?si=IfYOhiEJUE2TrBDb",
    "https://www.youtube.com/@youkushortfilm?si=aE0g_rOgRXYF2vUi",
    "https://www.youtube.com/@youkutaiwan?si=nlMAtT3_6aGQjPzg",
    "https://www.youtube.com/@youkuenglish?si=nwzlx1IgJnUwUkis",
    "https://www.youtube.com/@youkuenglishshorts?si=2WGJ8Rs3zNH8Gtwl",
    "https://www.youtube.com/@youkuthailand?si=rwEpUz35K2I06bvk",
    "https://www.youtube.com/@youkuthaimovie?si=I4juchFJofKNGAwo",
    "https://www.youtube.com/@youkuportuguese?si=agvDHw4ZioVgeWAw",
    "https://www.youtube.com/@youkuindonesia?si=PZxKOJ_NUgGFxfgP",
    "https://www.youtube.com/@youkuarabic?si=0NaJ2R1Tr0tpfuAL",
    "https://www.youtube.com/@youkuvietnam?si=L8naWnhCJPhxYTey",
    "https://www.youtube.com/@youkuspanish?si=ixloBH9pFxKibzxA",
    "https://www.youtube.com/@youkuphimle?si=RfaRNiCDWjyioaEa"
]
# urls = ["https://www.youtube.com/@youkuphimle?si=RfaRNiCDWjyioaEa"]

import requests
from requests.exceptions import RequestException, ConnectTimeout, SSLError
import time

# 要验证的网址（测试单个）
# urls = ["https://www.youtube.com/@tencentvideo"]

# 配置请求头（模拟浏览器，更完整）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}


def check_url_accessibility(url, proxies, timeout=15):
    """
    检查单个网址是否可访问（优化代理和请求方式）
    :param url: 要检查的网址
    :param proxies: 代理配置
    :param timeout: 超时时间（秒）
    :return: 状态（可访问/不可访问）、状态码、错误信息
    """
    try:
        # 改用 GET 请求（HEAD 请求可能被 YouTube 拦截）
        # 关闭重定向自动跟随，手动处理（避免代理下重定向异常）
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            proxies=proxies,
            allow_redirects=False,
            verify=False  # 忽略 SSL 证书验证（代理环境常见问题）
        )
        # YouTube 常见可访问状态码：200（正常）、301/302（重定向到频道）、429（请求限流）
        if response.status_code in [200, 301, 302]:
            return "可访问", response.status_code, ""
        elif response.status_code == 429:
            return "不可访问", response.status_code, "请求频率过高，YouTube 限流"
        else:
            return "不可访问", response.status_code, f"状态码：{response.status_code}"
    except ConnectTimeout:
        return "不可访问", 0, "连接超时（代理错误/网络不通）"
    except SSLError:
        return "不可访问", 0, "SSL 证书错误（建议检查代理或开启 verify=False）"
    except RequestException as e:
        error_detail = str(e)[:100]  # 显示更多错误信息
        return "不可访问", 0, f"请求异常：{error_detail}"


def batch_check_urls(url_list):
    """批量检查网址，并去重"""
    # 第一步：去重
    unique_urls = list(set(url_list))
    print(f"📊 原始网址数量：{len(url_list)} | 去重后数量：{len(unique_urls)}\n")

    # 第二步：配置代理（核心！必须和你的代理软件端口一致）
    proxies = {
        "http": "http://127.0.0.1:7897",
        "https": "http://127.0.0.1:7897"
    }

    # 第三步：批量检查
    results = []
    success_count = 0
    fail_count = 0

    for idx, url in enumerate(unique_urls, 1):
        print(f"正在检查 [{idx}/{len(unique_urls)}]：{url}")
        status, code, error = check_url_accessibility(url, proxies)
        results.append({
            "url": url,
            "status": status,
            "status_code": code,
            "error": error
        })

        if status == "可访问":
            success_count += 1
        else:
            fail_count += 1

        time.sleep(1)  # 延长延迟，避免 YouTube 限流

    # 第四步：输出结果
    print("\n" + "=" * 80)
    print("✅ 检查结果汇总：")
    print(f"可访问的网址数量：{success_count}")
    print(f"❌ 不可访问的网址数量：{fail_count}")
    print("=" * 80 + "\n")

    print("📋 详细检查结果：")
    for res in results:
        print(f"URL: {res['url']}")
        print(f"状态: {res['status']} | 状态码: {res['status_code']} | 错误信息: {res['error']}")
        print("-" * 80)

    return results


# 执行检查
if __name__ == "__main__":
    batch_check_urls(urls)
