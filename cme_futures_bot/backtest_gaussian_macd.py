import pandas as pd
from strategy_gaussian_macd import analyze

def main():
    # Load historical data
    df = pd.read_csv("historical_data.csv", parse_dates=["Date"])
    df.set_index("Date", inplace=True)

    # Run strategy
    result_df = analyze(df)

    # Display preview
    print(result_df.tail(10))

    # Save to CSV
    result_df.to_csv("gaussian_macd_backtest_results.csv")
    print("\\n✅ Backtest complete. Results saved to 'gaussian_macd_backtest_results.csv'.")

if __name__ == "__main__":
    main()
