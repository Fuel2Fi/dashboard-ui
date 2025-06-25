import ccxt
import pandas as pd

def fetch_binance_data(symbol: str, timeframe: str = '1h', limit: int = 200):
    exchange = ccxt.binanceus()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
def fetch_from_binance():
    tokens = {
        'bitcoin': 'BTC/USDT',
        'ethereum': 'ETH/USDT',
        'tether': 'USDT/USDT',
        'ripple': 'XRP/USDT',
        'binancecoin': 'BNB/USDT'
    }

    prices = {}
    for name, symbol in tokens.items():
        try:
            df = fetch_binance_data(symbol, limit=1)
            if not df.empty:
                prices[name] = float(df['close'].iloc[-1])
        except Exception as e:
            print(f"❌ Failed to fetch {name}: {e}")
    return prices

def fetch_from_binance():
    tokens = {
        'bitcoin': 'BTC/USDT',
        'ethereum': 'ETH/USDT',
        'ripple': 'XRP/USDT',
        'binancecoin': 'BNB/USDT'
        # 'tether' removed — not a valid pair on Binance.US
    }

    prices = {}
    for name, symbol in tokens.items():
        try:
            df = fetch_binance_data(symbol, limit=1)
            if not df.empty:
                prices[name] = float(df['close'].iloc[-1])
        except Exception as e:
            print(f"❌ Failed to fetch {name}: {e}")
    return prices
