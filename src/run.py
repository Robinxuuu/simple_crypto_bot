import os, json, time
from loguru import logger
from config import CRYPTOPANIC_API_KEY, EXCHANGE, SYMBOLS, TIMEFRAME, LOOKBACK_HOURS
from news_fetcher import fetch_news
from quant_fetcher import fetch_market_data
from analyzer import merge_and_summarize
from tts_engine import speak

def mk_run_dir():
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join("runs", ts)
    os.makedirs(path, exist_ok=True)
    return path

def main():
    run_dir = mk_run_dir()
    logger.add(os.path.join(run_dir, "agent.log"))

    logger.info("Step 1: 拉新闻")
    print("现在开始抓取新闻...")
    news_json = fetch_news(CRYPTOPANIC_API_KEY, limit=5)
    json.dump(news_json, open(os.path.join(run_dir,"news.json"),"w"), ensure_ascii=False, indent=2)
    logger.info(f"新闻条数: {len(news_json.get('news',[]))}")

    logger.info("Step 2: 拉行情+指标")
    print("现在开始抓取市场行情...")
    quants_json = fetch_market_data(SYMBOLS, EXCHANGE, TIMEFRAME, LOOKBACK_HOURS)
    json.dump(quants_json, open(os.path.join(run_dir,"quants.json"),"w"), ensure_ascii=False, indent=2)

    logger.info("Step 3: 合并并生成播报稿")
    print("信息抓取成功！生成播报中...")
    merged = merge_and_summarize(news_json, quants_json)
    json.dump(merged, open(os.path.join(run_dir,"merged.json"),"w"), ensure_ascii=False, indent=2)

    logger.info("Step 4: 播报")
    print("接下来是加密货币的市场播报...")
    speak(merged["script_cn"])
    print("\n=== 播报稿（备份） ===\n", merged["script_cn"])

if __name__ == "__main__":
    main()