import pandas as pd
from strategy_selector import run_selected_strategy

def main():
    # Load historical data
    df = pd.read_csv("historical_data.csv", parse_dates=["Date"])
    df.set_index("Date", inplace=True)

    # Pick which strategy to test here:
    strategy = "breakout"

    # Run the selected strategy
    result_df = run_selected_strategy(df, strategy)

    # Display results
    print(result_df.tail(10))

    # Save results
    result_df.to_csv(f"{strategy}_selector_backtest_results.csv")
    print(f"\\n✅ Backtest complete. Results saved to '{strategy}_selector_backtest_results.csv'.")

if __name__ == "__main__":
    main()
