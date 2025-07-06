import pandas as pd
from strategy_selector import run_selected_strategy
from consensus_engine import get_consensus_signal

def main():
    # Load data
    df = pd.read_csv("historical_data.csv", parse_dates=["Date"])
    df.set_index("Date", inplace=True)

    # Run selected strategies
    breakout_df = run_selected_strategy(df, "breakout")
    trend_df = run_selected_strategy(df, "trend_following")
    mean_df = run_selected_strategy(df, "mean_reversion")

    # Package results
    strategy_results = {
        "breakout": breakout_df,
        "trend_following": trend_df,
        "mean_reversion": mean_df
    }

    # Get consensus
    consensus_df = get_consensus_signal(strategy_results, required_agreement=2)

    # Show preview
    print(consensus_df.tail(20))

    # Save to CSV
    consensus_df.to_csv("consensus_signals.csv")
    print("\n✅ Consensus signals saved to 'consensus_signals.csv'.")

if __name__ == "__main__":
    main()
