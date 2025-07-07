import pandas as pd

def select_strategies():
    summary_df = pd.read_csv("auto_tuning_summary.csv")
    summary_df = summary_df.sort_values(by="Sharpe Ratio", ascending=False)

    # Print all strategies and their Sharpe
    print("\n✅ Strategy Switcher Selection:")
    for idx, row in enumerate(summary_df.itertuples(index=False), 1):
        print(f"{idx}. {row.Strategy} - Sharpe: {row._2:.2f}")

    # Return a list of tuples (strategy name, Sharpe Ratio)
    return list(zip(summary_df.head(3)["Strategy"], summary_df.head(3)["Sharpe Ratio"]))
