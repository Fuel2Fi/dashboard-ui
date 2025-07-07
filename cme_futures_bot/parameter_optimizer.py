import pandas as pd
import numpy as np
import itertools
import json

# Load your historical data
df = pd.read_csv("your_price_data.csv", parse_dates=["Date"])

# Drop rows with missing Close prices
df = df.dropna(subset=["Close"])

# Define parameter grid
fast_ma_range = [5, 10, 15]
slow_ma_range = [20, 50, 100]
rsi_thresholds = [30, 50, 70]

# Prepare results storage
results = []

# Loop through parameter combinations
for fast_ma, slow_ma, rsi_thresh in itertools.product(fast_ma_range, slow_ma_range, rsi_thresholds):
    if fast_ma >= slow_ma:
        continue  # skip invalid combinations

    # Compute indicators
    df["FastMA"] = df["Close"].rolling(fast_ma).mean()
    df["SlowMA"] = df["Close"].rolling(slow_ma).mean()
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    RS = gain / loss
    df["RSI"] = 100 - (100 / (1 + RS))

    # Generate signals
    df["Signal"] = np.where(
        (df["FastMA"] > df["SlowMA"]) & (df["RSI"] > rsi_thresh), "BUY",
        np.where((df["FastMA"] < df["SlowMA"]) & (df["RSI"] < (100 - rsi_thresh)), "SELL", "HOLD")
    )

    # Simulate returns
    df["Return"] = df["Close"].pct_change().shift(-1)
    df["StrategyReturn"] = np.where(df["Signal"] == "BUY", df["Return"],
                             np.where(df["Signal"] == "SELL", -df["Return"], 0))

    # Calculate stats
    cumulative_return = (1 + df["StrategyReturn"].fillna(0)).prod() - 1
    pnl_std = df["StrategyReturn"].std()
    sharpe = (df["StrategyReturn"].mean() / pnl_std) * np.sqrt(252) if pnl_std > 0 else 0
    wins = df[df["StrategyReturn"] > 0]
    total_trades = len(df[df["Signal"].isin(["BUY", "SELL"])])
    win_rate = len(wins) / total_trades * 100 if total_trades > 0 else 0

    # Log results
    results.append({
        "FastMA": fast_ma,
        "SlowMA": slow_ma,
        "RSI": rsi_thresh,
        "Sharpe": sharpe,
        "WinRate": win_rate,
        "CumulativeReturn": cumulative_return
    })

    print(f"✅ Tested FastMA={fast_ma}, SlowMA={slow_ma}, RSI={rsi_thresh} | Sharpe={sharpe:.2f}")

# Save results to CSV
results_df = pd.DataFrame(results)
results_df.sort_values(by="Sharpe", ascending=False).to_csv("parameter_optimization_results.csv", index=False)

# Save best parameters to JSON
best_params = results_df.sort_values(by="Sharpe", ascending=False).iloc[0].to_dict()
with open("best_parameters.json", "w") as f:
    json.dump(best_params, f, indent=4)

print("\n🎯 Optimization complete. Best parameters saved to 'best_parameters.json'.")
