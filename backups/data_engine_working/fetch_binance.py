import ccxt
import pandas as pd
from datetime import datetime

def fetch_binance_data(symbol='BTC/USDT', timeframe='1h', limit=100):
    exchange = ccxt.binanceus()  # IMPORTANT: using binance.us
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

