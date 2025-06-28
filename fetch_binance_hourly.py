#!/usr/bin/env python3

"""
fetch_binance_hourly.py
Fetches all available hourly OHLC data for selected tokens from Binance.US.
"""

import requests
import pandas as pd
import os
import time
from datetime import datetime

# Output directory
output_dir = "./data_hourly"
os.makedirs(output_dir, exist_ok=True)

# Base URL
base_url = "https://api.binance.us/api/v3/klines"

# Tokens
pairs = [
    {"symbol": "BTCUSDT"},
    {"symbol": "ETHUSDT"},
    {"symbol": "BNBUSDT"},
    {"symbol": "SOLUSDT"},
    {"symbol": "ADAUSDT"}
]

# Max records per request
limit = 1000

# Start date (adjust as needed)
start_date = datetime(2021, 1, 1)
end_date = datetime.utcnow()

# Convert to ms timestamps
start_ts = int(start_date.timestamp() * 1000)
end_ts = int(end_date.timestamp() * 1000)

interval = "1h"

for pair in pairs:
    print(f"Fetching {pair['symbol']}...")

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
            print(f"Error: {e}")
            break

        if not data:
            break

        all_data.extend(data)

        if len(data) < limit:
            break

        last_timestamp = data[-1][0]
        fetch_start = last_timestamp + 1

        time.sleep(0.2)

    if not all_data:
        print(f"No data for {pair['symbol']}.")
        continue

    df = pd.DataFrame(all_data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
    ])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df.set_index("open_time", inplace=True)
    df = df[["open", "high", "low", "close", "volume"]].astype(float)

    out_path = os.path.join(output_dir, f"{pair['symbol']}_hourly_ohlc.csv")
    df.to_csv(out_path)

    print(f"Saved {len(df)} records to {out_path}")

print("\n✅ All hourly data fetched.")
