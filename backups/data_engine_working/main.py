import pandas as pd
from fetch_binance import fetch_binance_data
from fetch_coinbase import fetch_coinbase_data
from fetch_coingecko import fetch_coingecko_data
from fetch_coinstats import fetch_coinstats_data
from fetch_cmc import fetch_cmc_data

# === Settings ===
symbol = 'BTC/USDT'
timeframe = '1h'
limit = 100

# === Fetch Data from All Sources ===
def fetch_all_data():
    dataframes = []

    try:
        df_binance = fetch_binance_data(symbol, timeframe, limit)
        if not df_binance.empty:
            dataframes.append(df_binance)
    except Exception as e:
        print(f"Binance failed: {e}")

    try:
        df_coinbase = fetch_coinbase_data(symbol, timeframe, limit)
        if not df_coinbase.empty:
            dataframes.append(df_coinbase)
    except Exception as e:
        print(f"Coinbase failed: {e}")

    try:
        df_coingecko = fetch_coingecko_data(symbol, timeframe, limit)
        if not df_coingecko.empty:
            dataframes.append(df_coingecko)
    except Exception as e:
        print(f"CoinGecko failed: {e}")

    try:
        df_coinstats = fetch_coinstats_data(symbol)
        if not df_coinstats.empty:
            dataframes.append(df_coinstats)
    except Exception as e:
        print(f"CoinStats failed: {e}")

    try:
        df_cmc = fetch_cmc_data(symbol)
        if not df_cmc.empty:
            dataframes.append(df_cmc)
    except Exception as e:
        print(f"CoinMarketCap failed: {e}")

    return merge_dataframes(dataframes)

# === Merge and Average Data ===
def merge_dataframes(dfs):
    if not dfs:
        raise Exception("No dataframes to merge.")

    merged = pd.concat(dfs)
    merged = merged.groupby('timestamp').agg({
        'open': 'mean',
        'high': 'mean',
        'low': 'mean',
        'close': 'mean',
        'volume': 'sum'
    }).reset_index()
    return merged

# === Run Script ===
if __name__ == '__main__':
    try:
        df = fetch_all_data()
        print("\n=== Blended Market Data (Last 10 Rows) ===")
        print(df.tail(10))
    except Exception as e:
        print(f"Exception while fetching data: {e}")

