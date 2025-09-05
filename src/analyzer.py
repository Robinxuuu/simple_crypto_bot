def simple_bias(latest_rsi, macd, macd_signal, bb_pos):
    # 非投资建议，仅演示规则
    if latest_rsi is None or bb_pos is None:
        return "neutral"
    if latest_rsi > 65 and macd > macd_signal and bb_pos > 0.6:
        return "bull"
    if latest_rsi < 35 and macd < macd_signal and bb_pos < 0.4:
        return "bear"
    return "neutral"

def merge_and_summarize(news_json, quants_json):
    per_symbol = {}
    bullets = []
    top_news = news_json.get("news", [])[:3]

    # 逐币种做一个极简倾向
    for m in quants_json.get("markets", []):
        sym = m["symbol"]
        latest = m["candles"][-1]
        bias = simple_bias(latest.get("rsi14"), latest.get("macd"), latest.get("macd_signal"),
                           m["signal_note"].get("bb_pos"))
        rationale = f"RSI={round(latest.get('rsi14',0),1)}, MACD{'>' if latest.get('macd',0)>latest.get('macd_signal',0) else '<='}Signal, 布林带位置~{round(m['signal_note'].get('bb_pos',0.5),2)}"
        per_symbol[sym] = {"bias": bias, "rationale": rationale,
                           "levels":{"rsi": round(latest.get("rsi14",0),1),
                                     "macd": "bull" if latest.get("macd",0)>latest.get("macd_signal",0) else "bear",
                                     "bb_pos": round(m['signal_note'].get('bb_pos',0.5),2)}}

    bullets.append("已汇总近24小时加密热点新闻与近48小时行情指标（1h）。")
    bullets.append("规则仅作信息展示，非投资建议。")

    # 生成60–90秒中文播报稿（模板）
    lines = ["这里是市场快讯。"]
    for sym, info in per_symbol.items():
        lines.append(f"{sym}：倾向 {info['bias']}，理由：{info['rationale']}。")
    if top_news:
        lines.append("相关新闻要点：")
        for n in top_news:
            lines.append(f"· {n['source']}：{n['title']}")
    lines.append("以上内容仅供参考，不构成投资建议。")
    script_cn = " ".join(lines)

    return {
      "summary_bullets": bullets,
      "per_symbol": per_symbol,
      "top_news": top_news,
      "script_cn": script_cn
    }

# 以下为包含模拟数据的测试代码
'''
if __name__ == "__main__":
    # 模拟新闻数据
    mock_news = {
        "news": [
            {
                "time": "2023-10-15T12:34:56Z",
                "title": "Bitcoin Surges Past $30,000 Amid Positive Market Sentiment",
                "source": "CryptoPanic",
                "summary": "Bitcoin price analysis and market sentiment",
                "tickers": ["BTC"],
                "sentiment": "neu"
            },
            {
                "time": "2023-10-15T11:23:45Z",
                "title": "Ethereum Network Upgrade Scheduled for Next Week",
                "source": "CryptoPanic",
                "summary": "Ethereum upcoming network upgrade details",
                "tickers": ["ETH"],
                "sentiment": "neu"
            }
        ]
    }

    # 模拟市场数据
    mock_quants = {
        "markets": [
            {
                "symbol": "BTC/USDT",
                "timeframe": "1h",
                "lookback_hours": 48,
                "asof": "2023-10-15T13:00:00Z",
                "signal_note": {
                    "rsi_note": "超买(>70)",
                    "macd_note": "多头",
                    "bb_pos": 0.68
                },
                "candles": [
                    {
                        "time": "2023-10-15T12:00:00Z",
                        "open": 29500.0,
                        "high": 30200.0,
                        "low": 29450.0,
                        "close": 30150.0,
                        "volume": 1234.56,
                        "rsi14": 67.2,
                        "macd": 125.6,
                        "macd_signal": 120.3,
                        "bb_lower": 29000.0,
                        "bb_mid": 29500.0,
                        "bb_upper": 30500.0
                    }
                    # 更多K线数据...
                ]
            },
            {
                "symbol": "ETH/USDT",
                "timeframe": "1h",
                "lookback_hours": 48,
                "asof": "2023-10-15T13:00:00Z",
                "signal_note": {
                    "rsi_note": "中性",
                    "macd_note": "空头",
                    "bb_pos": 0.45
                },
                "candles": [
                    {
                        "time": "2023-10-15T12:00:00Z",
                        "open": 1800.0,
                        "high": 1820.0,
                        "low": 1790.0,
                        "close": 1810.0,
                        "volume": 567.89,
                        "rsi14": 52.1,
                        "macd": -12.3,
                        "macd_signal": -10.5,
                        "bb_lower": 1750.0,
                        "bb_mid": 1800.0,
                        "bb_upper": 1850.0
                    }
                    # 更多K线数据...
                ]
            }
        ]
    }

    # 调用函数
    result = merge_and_summarize(mock_news, mock_quants)

    # 打印结果
    print("摘要要点:")
    for bullet in result["summary_bullets"]:
        print(f"- {bullet}")

    print("\n各交易对分析:")
    for symbol, analysis in result["per_symbol"].items():
        print(f"{symbol}: {analysis}")

    print("\n播报稿:")
    print(result["script_cn"])
'''