import os
import json
import pandas as pd

DATA_DIR = './data'

def load_token_data(token_symbol):
    filepath = os.path.join(DATA_DIR, f"{token_symbol}.json")
    with open(filepath, 'r') as f:
        data = json.load(f)
    # Expecting data as list of candles, each with close price and volume
    # Adjust keys if needed based on your JSON structure
    records = []
    for entry in data:
        # Assume entry has 'close' and 'volume' fields; adapt if different
        records.append({
            'timestamp': entry.get('close_time', entry.get('timestamp')),
            'close': float(entry['close']),
            'volume': float(entry['volume'])
        })
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df = df.sort_index()
    df.rename(columns={'close': f'{token_symbol}_close', 'volume': f'{token_symbol}_volume'}, inplace=True)
    return df

def load_all_tokens(token_symbols):
    dfs = []
    for token in token_symbols:
        try:
            df = load_token_data(token)
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {token}: {e}")
    if not dfs:
        raise RuntimeError("No data loaded. Check your JSON files in the data folder.")
    combined_df = pd.concat(dfs, axis=1).dropna()
    return combined_df

if __name__ == "__main__":
    tokens = ['BTCUSDT', 'ETHUSDT', 'XCNUSDT', 'COOKIEUSDT', 'TOSHIUSDT', 'XRPUSDT', 'SOLUSDT']
    df = load_all_tokens(tokens)
    print(df.head())
