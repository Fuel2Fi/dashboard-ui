import pandas as pd
import os

# Strategies to tune
strategies = [
    "trend_following",
    "mean_reversion",
    "breakout",
    "rsi_divergence",
    "gaussian_macd"
]

summary_rows = []

for strat in strategies:
    log_file = f"{strat}_performance_log.csv"
    if not os.path.exists(log_file):
        print(f"⚠️ Log file not found for {strat}. Skipping.")
        continue

    df = pd.read_csv(log_file)
    df = df.dropna(subset=["P&L"])

    total_trades = len(df)
    wins = df[df["P&L"] > 0]
    win_rate = len(wins) / total_trades * 100 if total_trades > 0 else 0
    avg_pnl = df["P&L"].mean() if total_trades > 0 else 0
    pnl_std = df["P&L"].std() if total_trades > 0 else 0
    sharpe = (avg_pnl / pnl_std) * (252 ** 0.5) if pnl_std > 0 else 0

    summary_rows.append({
        "Strategy": strat,
        "Total Trades": total_trades,
        "Win Rate (%)": win_rate,
        "Average P&L": avg_pnl,
        "Sharpe Ratio": sharpe
    })

    print(f"✅ {strat} tuning complete - Sharpe: {sharpe:.2f}")

# Save summary CSV
summary_df = pd.DataFrame(summary_rows)
summary_df = summary_df.sort_values(by="Sharpe Ratio", ascending=False)
summary_df.to_csv("auto_tuning_summary.csv", index=False)

print("\n🎯 Auto-Tuning complete. Summary saved to 'auto_tuning_summary.csv'.")
