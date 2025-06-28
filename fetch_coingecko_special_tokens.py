#!/usr/bin/env python3

"""
fetch_coingecko_special_tokens.py
Fetches historical price data for XCN, Cookie DAO, and Toshi tokens from CoinGecko.
"""

import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import time

# Your CoinGecko API Key
API_KEY = "CG-Dmr9nrkm5dDzT3rW6NVVMv1v"  # <-- Replace this with your real API key

# Output directory
output_dir = "./data"
os.makedirs(output_dir, exist_ok=True)

# Tokens to fetch
tokens = [
    {"symbol": "XCN", "id": "chain-2"},
    {"symbol": "COOKIE", "id": "cookie"},
    {"symbol": "TOSHI", "id": "toshi"}
]

# HTTP headers with API key
headers = {
    "accept": "application/json",
    "x-cg-pro-api-key": API_KEY
}

# Calculate Unix timestamps for 2 years back to now
now = int(time.time())
two_years_ago = int((datetime.utcnow() - timedelta(days=730)).timestamp())

# Fetch historical market data for each token
for token in tokens:
    print(f"Fetching data for {token['symbol']}...")

    url = (
        f"https://api.coingecko.com/api/v3/coins/{token['id']}/market_chart/range"
        f"?vs_currency=usd&from={two_years_ago}&to={now}"
    )

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data for {token['symbol']}: {e}")
        continue

    # Convert prices to DataFrame
    prices = data.get("prices", [])
    if not prices:
        print(f"No price data found for {token['symbol']}.")
        continue

    df = pd.DataFrame(prices, columns=["timestamp", "price_usd"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    # Save to CSV
    output_path = os.path.join(output_dir, f"{token['symbol']}_historical.csv")
    df.to_csv(output_path)

    print(f"Saved {len(df)} records for {token['symbol']} to {output_path}")

print("✅ All token data fetch operations completed.")

