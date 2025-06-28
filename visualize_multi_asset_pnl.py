#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os

# List of symbols to include
symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]

# Initialize empty dict to hold DataFrames
dfs = {}

# Load each symbol's PnL CSV
for symbol in symbols:
    csv_path = f"./data/{symbol}_pnl.csv"
    if not os.path.exists(csv_path):
        print(f"⚠️ Warning: {csv_path} not found. Skipping.")
        continue
    df = pd.read_csv(csv_path)
    df["open_time"] = pd.to_datetime(df["open_time"])
    dfs[symbol] = df

# Check at least one asset loaded
if not dfs:
    print("❌ No PnL files found. Exiting.")
    exit(1)

# Plot cumulative returns
plt.figure(figsize=(12,8))

for symbol, df in dfs.items():
    plt.plot(df["open_time"], df["cumulative_return"], label=symbol)

plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.title("Cumulative Returns Over Time (Multi-Asset)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("./data/multi_asset_pnl_chart.png")
print("✅ Multi-asset chart saved to ./data/multi_asset_pnl_chart.png")
