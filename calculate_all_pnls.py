#!/usr/bin/env python3
import os
import pandas as pd

# Directory where your OHLC CSVs are stored
DATA_DIR = "./data"

# Find all files ending with _daily_ohlc.csv
ohlc_files = [f for f in os.listdir(DATA_DIR) if f.endswith("_daily_ohlc.csv")]

if not ohlc_files:
    print("❌ No OHLC files found in ./data/. Exiting.")
    exit(1)

for ohlc_file in ohlc_files:
    symbol = ohlc_file.replace("_daily_ohlc.csv", "")
    output_file = f"{DATA_DIR}/{symbol}_pnl.csv"

    print(f"✅ Processing {symbol}...")

    df = pd.read_csv(os.path.join(DATA_DIR, ohlc_file))

    if "open_time" not in df.columns or "close" not in df.columns:
        print(f"⚠️ Skipping {symbol}: Missing required columns.")
        continue

    df["open_time"] = pd.to_datetime(df["open_time"])

    # Calculate returns
    df["return"] = df["close"].pct_change()
    df["cumulative_return"] = (1 + df["return"]).cumprod() - 1

    # Save PnL file
    df[["open_time", "return", "cumulative_return"]].to_csv(output_file, index=False)
    print(f"✅ Saved {output_file}")

print("🎯 All PnL calculations completed.")
