import warnings
warnings.filterwarnings(
    "ignore",
    message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated",
    category=FutureWarning
)

import pandas as pd
from strategy_selector import run_selected_strategy
from consensus_engine import get_consensus_signal
from performance_tracker import PerformanceTracker

def main():
    # Load historical data
    df = pd.read_csv("historical_data.csv", parse_dates=["Date"])
    df.set_index("Date", inplace=True)

    # Define strategy performance summary files
    performance_csv_paths = {
        "trend_following": "trend_following_performance_summary.csv",
        "mean_reversion": "mean_reversion_performance_summary.csv",
        "breakout": "breakout_performance_summary.csv",
        "rsi_divergence": "rsi_divergence_performance_summary.csv",
        "gaussian_macd": "gaussian_macd_performance_summary.csv"
    }

    # Select top strategies
    from strategy_switcher import select_top_strategies
    top_strategies = select_top_strategies(performance_csv_paths, top_n=3)

    # Run selected strategies
    strategy_results = {}
    for strat in top_strategies:
        strat_df = run_selected_strategy(df, strat)
        strategy_results[strat] = strat_df

    # Compute consensus signal
    consensus_df = get_consensus_signal(strategy_results, required_agreement=2)

    # Display last 10 consensus signals
    print(consensus_df.tail(10))

    # Log simulated trades
    tracker = PerformanceTracker()
    for date, row in consensus_df.iterrows():
        signal = row["ConsensusSignal"]
        price = df.loc[date, "Close"]
        if signal != "HOLD":
            tracker.log_trade(
                date=date.strftime("%Y-%m-%d"),
                strategy="ConsensusEngine",
                signal=signal,
                entry_price=price,
                exit_price=None
            )

    # Compute and print stats
    stats = tracker.compute_stats()
    print("\n✅ Strategy Engine Run Complete.")
    print("📊 Performance Stats:")
    for k, v in stats.items():
        print(f"- {k}: {v}")

if __name__ == "__main__":
    main()
