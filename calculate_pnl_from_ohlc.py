#!/usr/bin/env python3
import pandas as pd

# Load OHLC data
ohlc_path = "./data/BTCUSDT_daily_ohlc.csv"
df = pd.read_csv(ohlc_path)

# Use the correct timestamp column
df["open_time"] = pd.to_datetime(df["open_time"])

# Sort just in case
df = df.sort_values("open_time")

# Example: Calculate simple returns
df["return"] = df["close"].pct_change()

# Cumulative returns
df["cumulative_return"] = (1 + df["return"]).cumprod()

# Save the results
output_path = "./data/BTCUSDT_pnl.csv"
df.to_csv(output_path, index=False)

print(f"✅ PnL calculations saved to {output_path}")

