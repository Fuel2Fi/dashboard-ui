import sys
import os
import json
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_sources.coingecko.token_config import TOKEN_LIST as COINGECKO_TOKENS
from data_sources.coingecko.fetch_coingecko import fetch_price_from_coingecko
from data_sources.binance_source import fetch_from_binance

def fetch_all_coingecko():
    prices = {}
    for token in COINGECKO_TOKENS:
        try:
            price = fetch_price_from_coingecko(token)
            if isinstance(price, (int, float)):
                prices[token] = price
                print(f"✅ [CoinGecko] {token:<15} | ${price}")
            else:
                print(f"❌ [CoinGecko] {token:<15} | No price returned")
        except Exception as e:
            print(f"❌ [CoinGecko] {token:<15} | ERROR: {e}")
        time.sleep(2.1)  # Stay under CoinGecko's Pro rate limit
    return prices

def merge_data(binance_data, coingecko_data):
    merged = {}
    for token in coingecko_data:
        if token in binance_data:
            merged[token] = {
                'binance': binance_data[token],
                'coingecko': coingecko_data[token],
                'average_price': round((binance_data[token] + coingecko_data[token]) / 2, 4)
            }
    return merged

if __name__ == "__main__":
    print("🔁 Merging Binance.US + CoinGecko feeds...\n")

    coingecko_data = fetch_all_coingecko()
    binance_data = fetch_from_binance()

    if not coingecko_data:
        print("❌ CoinGecko feed failed. Aborting.")
        exit(1)

    if not binance_data:
        print("❌ Binance.US feed failed. Aborting.")
        exit(1)

    merged = merge_data(binance_data, coingecko_data)

    if merged:
        print("\n✅ Merged data feed created successfully:\n")
        for token, data in merged.items():
            print(f"{token.title():<15} | Binance: ${data['binance']:<8} | CoinGecko: ${data['coingecko']:<8} | Avg: ${data['average_price']}")
        with open("merged_data.json", "w") as f:
            json.dump(merged, f, indent=2)
    else:
        print("⚠️ No matching tokens to merge.")
