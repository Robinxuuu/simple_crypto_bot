import ccxt, time
import pandas as pd
import pandas_ta as ta

def fetch_market_data(symbols, exchange="binance", timeframe="1h", lookback_hours=48):
    ex = getattr(ccxt, exchange)()
    out = {"markets":[]}
    limit = max(lookback_hours + 100, 200)
    for sym in symbols:
        ohlcv = ex.fetch_ohlcv(sym, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["ts","open","high","low","close","volume"]).tail(lookback_hours)
        df["time"] = pd.to_datetime(df["ts"], unit="ms", utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        df["rsi14"] = ta.rsi(df["close"], length=14)
        macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
        df["macd"] = macd["MACD_12_26_9"]
        df["macd_signal"] = macd["MACDs_12_26_9"]
        bb = ta.bbands(df["close"], length=20, std=2)
        df["bb_lower"], df["bb_mid"], df["bb_upper"] = bb["BBL_20_2.0"], bb["BBM_20_2.0"], bb["BBU_20_2.0"]
        latest = df.iloc[-1]
        band_pos = float((latest["close"]-latest["bb_lower"])/(latest["bb_upper"]-latest["bb_lower"])) if (latest["bb_upper"]-latest["bb_lower"]) else None
        signal_note = {
            "rsi_note": "超买(>70)" if latest["rsi14"] and latest["rsi14"]>70 else ("超卖(<30)" if latest["rsi14"] and latest["rsi14"]<30 else "中性"),
            "macd_note": "多头" if latest["macd"]>latest["macd_signal"] else "空头",
            "bb_pos": band_pos
        }
        candles = df[["time","open","high","low","close","volume","rsi14","macd","macd_signal","bb_lower","bb_mid","bb_upper"]].round(6).to_dict(orient="records")
        out["markets"].append({"symbol": sym, "timeframe": timeframe, "lookback_hours": lookback_hours,
                               "asof": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                               "signal_note": signal_note,
                               "candles": candles})
    return out


# 以下为测试代码
'''
if __name__ == "__main__":
    from config import SYMBOLS, EXCHANGE, TIMEFRAME, LOOKBACK_HOURS

    print("开始测试市场数据获取功能...")

    # 调用fetch_market_data函数
    result = fetch_market_data(SYMBOLS, EXCHANGE, TIMEFRAME, LOOKBACK_HOURS)

    print(f"成功获取到 {len(result['markets'])} 个交易对的数据:")

    # 打印每个交易对的基本信息和信号
    for market in result["markets"]:
        print(f"\n--- {market['symbol']} ---")
        print(f"时间框架: {market['timeframe']}")
        print(f"数据更新时间: {market['asof']}")
        print(f"RSI信号: {market['signal_note']['rsi_note']}")
        print(f"MACD信号: {market['signal_note']['macd_note']}")
        print(f"布林带位置: {market['signal_note']['bb_pos']}")

        # 打印最新一根K线的数据
        latest_candle = market["candles"][-1]
        print(f"最新收盘价: {latest_candle['close']}")
        print(f"最新RSI值: {latest_candle.get('rsi14', 'N/A')}")
'''