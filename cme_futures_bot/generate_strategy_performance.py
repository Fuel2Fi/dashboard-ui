import pandas as pd
from strategy_selector import run_selected_strategy
from performance_tracker import PerformanceTracker

def main():
    df = pd.read_csv("historical_data.csv", parse_dates=["Date"])
    df.set_index("Date", inplace=True)

    strategies = [
        "trend_following",
        "mean_reversion",
        "breakout",
        "rsi_divergence",
        "gaussian_macd"
    ]

    for strat in strategies:
        print(f"\n🚀 Processing {strat}...")

        strat_df = run_selected_strategy(df, strat)

        # Log trades
        tracker = PerformanceTracker(log_file=f"{strat}_performance_log.csv")

        entry_price = None
        for date, row in strat_df.iterrows():
            signal = row["Signal"]
            close = row["Close"]

            if signal == "BUY":
                entry_price = close
            elif signal == "SELL" and entry_price is not None:
                tracker.log_trade(
                    date=date.strftime("%Y-%m-%d"),
                    strategy=strat,
                    signal="BUY",
                    entry_price=entry_price,
                    exit_price=close
                )
                entry_price = None  # reset

        # Compute stats
        stats = tracker.compute_stats()
        summary_df = pd.DataFrame([{
            "Strategy": strat,
            "Sharpe": stats["Sharpe Ratio"],
            "Win Rate": stats["Win Rate (%)"],
            "Avg P&L": stats["Average P&L"]
        }])
        summary_df.to_csv(f"{strat}_performance_summary.csv", index=False)

        print(f"✅ Summary saved to {strat}_performance_summary.csv")

if __name__ == "__main__":
    main()
