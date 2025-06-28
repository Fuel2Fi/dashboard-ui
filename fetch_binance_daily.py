#!/usr/bin/env python3

"""
fetch_binance_daily.py
Fetches full daily historical candles for BTC, ETH, BNB, SOL, and ADA from Binance.US.
"""

import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import time

# Output directory
output_dir = "./data"
os.makedirs(output_dir, exist_ok=True)

# Base URL for Binance.US API
base_url = "https://api.binance.us/api/v3/klines"

# Token pairs to fetch
pairs = [
    {"symbol": "BTCUSDT"},
    {"symbol": "ETHUSDT"},
    {"symbol": "BNBUSDT"},
    {"symbol": "SOLUSDT"},
    {"symbol": "ADAUSDT"}
]

# Max limit per request
limit = 1000

# Start date (adjust as needed)
start_date = datetime(2017, 8, 17)  # earliest possible BTCUSDT date
end_date = datetime.utcnow()

# Convert to milliseconds
start_ts = int(start_date.timestamp() * 1000)
end_ts = int(end_date.timestamp() * 1000)

interval = "1d"

for pair in pairs:
    print(f"Fetching data for {pair['symbol']}...")

    all_data = []
    fetch_start = start_ts

    while True:
        params = {
            "symbol": pair["symbol"],
            "interval": interval,
            "startTime": fetch_start,
            "endTime": end_ts,
            "limit": limit
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Error fetching data for {pair['symbol']}: {e}")
            break

        if not data:
            break

        all_data.extend(data)

        # If fewer than limit, done
        if len(data) < limit:
            break

        # Advance start time
        last_timestamp = data[-1][0]
        fetch_start = last_timestamp + 1

        time.sleep(0.2)  # respectful delay

    if not all_data:
        print(f"No data returned for {pair['symbol']}.")
        continue

    # Convert to DataFrame
    df = pd.DataFrame(all_data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df.set_index("open_time", inplace=True)
    df = df[["open", "high", "low", "close", "volume"]].astype(float)

    # Save to CSV
    output_path = os.path.join(output_dir, f"{pair['symbol']}_daily_ohlc.csv")
    df.to_csv(output_path)

    print(f"Saved {len(df)} daily records for {pair['symbol']} to {output_path}")

print("✅ All Binance.US data fetch operations completed.")
