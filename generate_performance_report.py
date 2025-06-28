#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define assets
assets = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]

# Prepare report DataFrame
summary = []

plt.figure(figsize=(10,6))

for asset in assets:
    file_path = f"./data/{asset}_pnl.csv"
    if not os.path.exists(file_path):
        print(f"⚠️ {file_path} not found. Skipping.")
        continue

    df = pd.read_csv(file_path)
    df["open_time"] = pd.to_datetime(df["open_time"])
    df["drawdown"] = df["cumulative_return"] - df["cumulative_return"].cummax()

    total_return = df["cumulative_return"].iloc[-1]
    avg_daily_return = df["return"].mean()
    max_drawdown = df["drawdown"].min()

    summary.append({
        "Asset": asset,
        "Total Return (%)": round(total_return * 100, 2),
        "Average Daily Return (%)": round(avg_daily_return * 100, 2),
        "Max Drawdown (%)": round(max_drawdown * 100, 2)
    })

    # Plot cumulative return
    plt.plot(df["open_time"], df["cumulative_return"], label=asset)

# Save summary table
summary_df = pd.DataFrame(summary)
summary_df.to_csv("./data/performance_summary.csv", index=False)

# Plot formatting
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.title("Multi-Asset Performance Summary")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("./data/summary_report.png")

print("✅ Performance summary saved to ./data/performance_summary.csv")
print("✅ Summary chart saved to ./data/summary_report.png")
