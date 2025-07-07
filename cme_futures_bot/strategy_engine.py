import pandas as pd
from exit_engine import ExitStrategy

def main():
    # Load market data
    df = pd.read_csv("market_data.csv")

    # Initialize ExitStrategy
    exit_engine = ExitStrategy()

    # Performance tracking
    trade_log = []
    cumulative_profit = 0
    wins = 0
    losses = 0
    total_trades = 0
    current_entry_price = None

    for _, row in df.iterrows():
        price = row["Price"]
        date = row["Date"]

        if not exit_engine.in_position:
            if price > 1000:
                exit_engine.mark_entry(entry_price=price, date=date)
                current_entry_price = price
                status = "Entry triggered"
                print(f"✅ Entry triggered at {price} on {date}")
            else:
                status = "No action"
                print(f"✅ No action at {price} on {date}")
        else:
            exit_result = exit_engine.check_exit_signal(price, date)
            if exit_result:
                pnl = price - current_entry_price
                cumulative_profit += pnl
                total_trades += 1
                if pnl >= 0:
                    wins += 1
                else:
                    losses += 1
                status = f"Exit triggered (PnL: {pnl})"
                print(f"✅ Exit triggered at {price} on {date} (PnL: {pnl})")
                current_entry_price = None
            else:
                status = "Holding position"
                print(f"✅ Holding position at {price} on {date}")

        trade_log.append({
            "Date": date,
            "Price": price,
            "Status": status,
            "CumulativeProfit": cumulative_profit
        })

    # Save log to CSV
    log_df = pd.DataFrame(trade_log)
    log_df.to_csv("trade_performance_log.csv", index=False)

    # Compute summary
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    avg_return = (cumulative_profit / total_trades) if total_trades > 0 else 0

    print("\n🎯 Performance Summary")
    print("--------------------------")
    print(f"Total Trades: {total_trades}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Average Return per Trade: {avg_return:.2f}")
    print(f"Cumulative Profit: {cumulative_profit:.2f}")
    print("✅ Detailed log saved to trade_performance_log.csv")

if __name__ == "__main__":
    main()
