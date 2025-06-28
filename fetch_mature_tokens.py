#!/usr/bin/env python3

"""
fetch_mature_tokens.py
Fetches historical daily price data for BTC, ETH, BNB, SOL, and ADA from CoinGecko.
"""

import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import time

# Your CoinGecko API Key
API_KEY = "CG-Dmr9nrkm5dDzT3rW6NVVMv1v"  # <-- Replace this with your actual key

# Output directory
output_dir = "./data"
os.makedirs(output_dir, exist_ok=True)

# Tokens to fetch
tokens = [
    {"symbol": "BTC", "id": "bitcoin"},
    {"symbol": "ETH", "id": "ethereum"},
    {"symbol": "BNB", "id": "binancecoin"},
    {"symbol": "SOL", "id": "solana"},
    {"symbol": "ADA", "id": "cardano"}
]

# HTTP headers with API key
headers = {
    "accept": "application/json",
    "x-cg-pro-api-key": API_KEY
}

# Calculate Unix timestamps for 4 years back to now
now = int(time.time())
four_years_ago = int((datetime.utcnow() - timedelta(days=1460)).timestamp())

# Fetch historical market data for each token
for token in tokens:
    print(f"Fetching data for {token['symbol']}...")

    url = (
        f"https://api.coingecko.com/api/v3/coins/{token['id']}/market_chart/range"
        f"?vs_currency=usd&from={four_years_ago}&to={now}"
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

    # Resample to daily data (OHLC)
    daily_df = df["price_usd"].resample("1D").ohlc()

    # Save to CSV
    output_path = os.path.join(output_dir, f"{token['symbol']}_daily_ohlc.csv")
    daily_df.to_csv(output_path)

    print(f"Saved {len(daily_df)} daily records for {token['symbol']} to {output_path}")

print("✅ All token data fetch operations completed.")
