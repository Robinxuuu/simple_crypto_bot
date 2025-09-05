from dotenv import load_dotenv
import os
load_dotenv()

CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY", "")
EXCHANGE = os.getenv("EXCHANGE", "binance")
SYMBOLS = [s.strip() for s in os.getenv("SYMBOLS","BTC/USDT").split(",")]
TIMEFRAME = os.getenv("TIMEFRAME", "1h")
LOOKBACK_HOURS = int(os.getenv("LOOKBACK_HOURS","48"))