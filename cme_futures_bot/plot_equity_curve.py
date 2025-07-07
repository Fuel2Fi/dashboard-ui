import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load trade log
    df = pd.read_csv("trade_performance_log.csv")

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    plt.figure(figsize=(12, 6))

    # Plot cumulative profit
    plt.plot(df["Date"], df["CumulativeProfit"], linestyle="-", color="blue", label="Equity Curve")

    # Annotate entries and exits
    for idx, row in df.iterrows():
        date = row["Date"]
        profit = row["CumulativeProfit"]
        status = row["Status"]

        if "Entry" in status:
            plt.scatter(date, profit, color="green", marker="^", s=100, label="Entry" if "Entry" not in plt.gca().get_legend_handles_labels()[1] else "")
        elif "Exit" in status:
            plt.scatter(date, profit, color="red", marker="v", s=100, label="Exit" if "Exit" not in plt.gca().get_legend_handles_labels()[1] else "")
            # Extract PnL value from status text
            try:
                pnl_str = status.split("PnL:")[1].replace(")", "").strip()
                plt.text(date, profit - 50, f"{pnl_str}", color="black", fontsize=9, ha="center")
            except IndexError:
                pass  # No PnL info found

    plt.title("Equity Curve with Entry/Exit Annotations and PnL Labels")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Profit")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)

    # Save the figure
    plt.savefig("equity_curve_pnl_labels.png")
    print("✅ Annotated equity curve with PnL labels saved as equity_curve_pnl_labels.png")

if __name__ == "__main__":
    main()
