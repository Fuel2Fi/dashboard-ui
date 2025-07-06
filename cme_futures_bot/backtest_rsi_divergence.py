import pandas as pd
from strategy_rsi_divergence import analyze

def main():
    # Load historical data
    df = pd.read_csv("historical_data.csv", parse_dates=["Date"])
    df.set_index("Date", inplace=True)

    # Run RSI divergence strategy
    result_df = analyze(df)

    # Display last 10 signals
    print(result_df.tail(10))

    # Save results to CSV
    result_df.to_csv("rsi_divergence_backtest_results.csv")
    print("\\n✅ Backtest complete. Results saved to 'rsi_divergence_backtest_results.csv'.")

if __name__ == "__main__":
    main()
