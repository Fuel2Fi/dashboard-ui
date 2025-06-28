import requests
import json
import time
from datetime import datetime

def fetch_ohlcv(symbol='BTCUSDT', interval='1d', start_str='2017-01-01'):
    url = 'https://api.binance.com/api/v3/klines'
    limit = 1000
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': int(datetime.strptime(start_str, '%Y-%m-%d').timestamp() * 1000),
        'limit': limit
    }

    all_data = []
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        print(f"Fetched {len(data)} items")  # Debug output
        if not isinstance(data, list) or len(data) == 0:
            print(f"Received unexpected data: {data}")
            break
        all_data.extend(data)
        if len(data) < limit:
            break
        last_close_time = int(data[-1][6])  # Safely convert to int
        params['startTime'] = last_close_time + 1
        time.sleep(0.5)  # Rate limit compliance

    formatted_data = []
    for entry in all_data:
        # Validate entry structure before processing
        if not isinstance(entry, list) or len(entry) < 11:
            print(f"Skipping invalid entry: {entry}")
            continue
        try:
            formatted_data.append({
                'open_time': datetime.utcfromtimestamp(int(entry[0]) / 1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'open': float(entry[1]),
                'high': float(entry[2]),
                'low': float(entry[3]),
                'close': float(entry[4]),
                'volume': float(entry[5]),
                'close_time': datetime.utcfromtimestamp(int(entry[6]) / 1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'quote_asset_volume': float(entry[7]),
                'num_trades': int(entry[8]),
                'taker_buy_base_asset_volume': float(entry[9]),
                'taker_buy_quote_asset_volume': float(entry[10]),
            })
        except Exception as e:
            print(f"Error parsing entry {entry}: {e}")
            continue

    return formatted_data

if __name__ == "__main__":
    data = fetch_ohlcv(symbol='BTCUSDT', interval='1d', start_str='2017-01-01')
    with open('binance_historical_data_extended.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Fetched {len(data)} candles of BTCUSDT daily data starting from 2017-01-01.")
