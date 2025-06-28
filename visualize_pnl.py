#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

# Load the PnL CSV
df = pd.read_csv("./data/BTCUSDT_pnl.csv")

# Convert timestamp
df["open_time"] = pd.to_datetime(df["open_time"])

# Basic statistics
total_return = df["cumulative_return"].iloc[-1]
average_daily_return = df["return"].mean()

print(f"✅ Total Cumulative Return: {total_return:.2%}")
print(f"✅ Average Daily Return: {average_daily_return:.2%}")

# Plot cumulative return
plt.figure(figsize=(10,6))
plt.plot(df["open_time"], df["cumulative_return"], label="Cumulative Return")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.title("BTCUSDT Cumulative Return Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("./data/pnl_chart.png")
print("✅ Chart saved to ./data/pnl_chart.png")
