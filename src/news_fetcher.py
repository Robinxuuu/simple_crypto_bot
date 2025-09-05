import requests, datetime

def fetch_news(api_key: str, limit: int = 5):
    """返回标准化新闻：time/title/source/summary/tickers/sentiment"""
    if not api_key:
        return {"news":[]}
    url = "https://cryptopanic.com/api/developer/v2/posts/"     # 以官方文档为准
    params = {
        "auth_token": api_key,
        "kind": "news",
        "public": "true",
        "filter": "hot",   # 或 rising / bullish / bearish 等
        "currencies": "BTC,ETH,SOL",
        "limit": limit
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    items = []
    for p in data.get("results", [])[:limit]:
        items.append({
            "time": p.get("published_at") or datetime.datetime.utcnow().isoformat()+"Z",
            "title": p.get("title","").strip(),
            "source": "CryptoPanic",
            "summary": p.get("description",""),  # 简要占位
            "tickers": [c for c in (p.get("currencies") or []) if isinstance(c, str)],
            "sentiment": "neu"  # 新手阶段先统一中性，后面再做细分
        })
    return {"news": items}

# 以下为测试代码
'''
if __name__ == "__main__":
    # 从config模块导入配置
    from config import CRYPTOPANIC_API_KEY

    print("开始测试新闻获取功能...")

    # 调用fetch_news函数
    result = fetch_news(CRYPTOPANIC_API_KEY, limit=3)

    print(f"成功获取到 {len(result['news'])} 条新闻:")

    # 打印每条新闻的详细信息
    for i, news_item in enumerate(result['news']):
        print(f"\n--- 新闻 #{i + 1} ---")
        print(f"时间: {news_item['time']}")
        print(f"标题: {news_item['title']}")
        print(f"来源: {news_item['source']}")
        print(f"摘要: {news_item['summary']}")
        print(f"相关代币: {news_item['tickers']}")    #暂时留空
        print(f"情感倾向: {news_item['sentiment']}")  #暂时留空
'''