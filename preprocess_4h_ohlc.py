#!/usr/bin/env python3
import os
import pandas as pd

# Folder paths
input_folder = "./data_hourly"
output_folder = "./data_4h"
os.makedirs(output_folder, exist_ok=True)

symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]

for symbol in symbols:
    input_path = os.path.join(input_folder, f"{symbol}_hourly_ohlc.csv")
    output_path = os.path.join(output_folder, f"{symbol}_4h_ohlc.csv")
    
    if not os.path.exists(input_path):
        print(f"⚠️ Missing hourly data for {symbol}. Skipping.")
        continue

    df = pd.read_csv(input_path)
    df["open_time"] = pd.to_datetime(df["open_time"])
    df.set_index("open_time", inplace=True)

    df_4h = df.resample("4H").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }).dropna()

    df_4h.reset_index(inplace=True)
    df_4h.to_csv(output_path, index=False)
    print(f"✅ Saved 4H OHLC for {symbol} -> {output_path}")
