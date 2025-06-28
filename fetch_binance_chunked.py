import requests
import json
import time
from datetime import datetime, timedelta

def fetch_ohlcv_chunked(symbol='BTCUSDT', interval='1d', start_str='2023-01-01', end_str=None):
    base_url = 'https://api.binance.us/api/v3/klines'
    start = datetime.strptime(start_str, '%Y-%m-%d')
    end = datetime.strptime(end_str, '%Y-%m-%d') if end_str else datetime.utcnow()
    
    all_data = []
    limit = 1000  # max per request

    while start < end:
        # Calculate chunk end date (max 1000 candles per request)
        chunk_end = start + timedelta(days=limit)
        if chunk_end > end:
            chunk_end = end

        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': int(start.timestamp() * 1000),
            'endTime': int(chunk_end.timestamp() * 1000),
            'limit': limit
        }

        print(f"Fetching data from {start.strftime('%Y-%m-%d')} to {chunk_end.strftime('%Y-%m-%d')} ...")
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            break

        data = response.json()
        if not data:
            print("No data returned, stopping.")
            break

        all_data.extend(data)
        start = chunk_end + timedelta(milliseconds=1)  # move start past last chunk

        time.sleep(0.5)  # rate limit safety pause

    # Format data nicely
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
    # Example: Fetch BTCUSDT daily data from 2020-01-01 to 2023-12-31
    data = fetch_ohlcv_chunked(symbol='BTCUSDT', interval='1d', start_str='2020-01-01', end_str='2023-12-31')
    with open('binance_btc_3yrs_chunked.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Fetched {len(data)} candles of BTCUSDT daily data from 2020-01-01 to 2023-12-31.")
