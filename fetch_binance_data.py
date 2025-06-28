import requests
import time
import json
from datetime import datetime

def fetch_ohlcv(symbol='BTCUSDT', interval='1d', start_str=None, limit=1000):
    base_url = 'https://api.binance.us/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit,
    }
    if start_str:
        start_ts = int(datetime.strptime(start_str, '%Y-%m-%d').timestamp() * 1000)
        params['startTime'] = start_ts

    all_data = []
    while True:
        response = requests.get(base_url, params=params)
        data = response.json()
        if not data:
            break
        all_data.extend(data)
        if len(data) < limit:
            break
        last_close_time = data[-1][6]
        params['startTime'] = last_close_time + 1
        time.sleep(0.5)  # Respect rate limits

    formatted_data = []
    for entry in all_data:
        formatted_data.append({
            'open_time': datetime.utcfromtimestamp(entry[0] / 1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'open': float(entry[1]),
            'high': float(entry[2]),
            'low': float(entry[3]),
            'close': float(entry[4]),
            'volume': float(entry[5]),
            'close_time': datetime.utcfromtimestamp(entry[6] / 1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'quote_asset_volume': float(entry[7]),
            'num_trades': int(entry[8]),
            'taker_buy_base_asset_volume': float(entry[9]),
            'taker_buy_quote_asset_volume': float(entry[10]),
        })
    return formatted_data

if __name__ == "__main__":
    data = fetch_ohlcv(symbol='BTCUSDT', interval='1d', start_str='2023-01-01')
    with open('binance_historical_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Fetched {len(data)} candles of BTCUSDT daily data starting from 2023-01-01.")

