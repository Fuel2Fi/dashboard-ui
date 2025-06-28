import requests
import json
from datetime import datetime

def fetch_coingecko_ohlcv(coin_id='bitcoin', vs_currency='usd', days='max'):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': vs_currency,
        'days': days,
        'interval': 'daily'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Fuel2FiBot/1.0; +https://fuel2fi.com)'
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response content: {response.text}")
        return []
    data = response.json()

    prices = data.get('prices', [])
    if not prices:
        print("Warning: No price data found in response.")
    formatted_data = []
    for price in prices:
        timestamp_ms, price_value = price
        timestamp = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')
        formatted_data.append({
            'timestamp': timestamp,
            'price': price_value
        })
    return formatted_data

if __name__ == "__main__":
    data = fetch_coingecko_ohlcv(days='max')  # fetch all available data
    with open('coingecko_btc_max.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Fetched {len(data)} days of BTC price data from CoinGecko.")
