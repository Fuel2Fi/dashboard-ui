import requests
import json
import time
from datetime import datetime

def fetch_ohlcv(symbol, interval='1d', start_str='2023-01-01'):
    url = 'https://api.binance.us/api/v3/klines'
    start_ts = int(datetime.strptime(start_str, '%Y-%m-%d').timestamp() * 1000)
    limit = 1000
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_ts,
        'limit': limit
    }
    all_data = []
    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error fetching {symbol}: {response.status_code} {response.text}")
            break
        data = response.json()
        if not data:
            break
        all_data.extend(data)
        if len(data) < limit:
            break
        last_close_time = data[-1][6]
        params['startTime'] = last_close_time + 1
        time.sleep(0.5)
    formatted = []
    for entry in all_data:
        formatted.append({
            'open_time': datetime.utcfromtimestamp(entry[0]/1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'open': float(entry[1]),
            'high': float(entry[2]),
            'low': float(entry[3]),
            'close': float(entry[4]),
            'volume': float(entry[5]),
            'close_time': datetime.utcfromtimestamp(entry[6]/1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'quote_asset_volume': float(entry[7]),
            'num_trades': int(entry[8]),
            'taker_buy_base_asset_volume': float(entry[9]),
            'taker_buy_quote_asset_volume': float(entry[10]),
        })
    return formatted

if __name__ == "__main__":
    tokens = [
        {'name': 'Bitcoin', 'symbol': 'BTCUSDT'},
        {'name': 'Ethereum', 'symbol': 'ETHUSDT'},
        {'name': 'XRP', 'symbol': 'XRPUSDT'},
        {'name': 'Solana', 'symbol': 'SOLUSDT'}
    ]
    start_date = '2023-01-01'

    for token in tokens:
        print(f"Fetching data for {token['name']} ({token['symbol']}) from {start_date}...")
        data = fetch_ohlcv(token['symbol'], start_str=start_date)
        with open(f"./data/{token['symbol']}.json", 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} candles for {token['symbol']} to ./data/{token['symbol']}.json")
