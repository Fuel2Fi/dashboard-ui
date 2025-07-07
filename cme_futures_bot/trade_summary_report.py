import pandas as pd
import json

class ExitStrategy:
    def __init__(self, trailing_threshold_pct):
        self.trailing_threshold_pct = trailing_threshold_pct
        self.high_price = None
        self.in_position = False

    def mark_entry(self, entry_price):
        self.in_position = True
        self.high_price = entry_price

    def check_exit_signal(self, price):
        if not self.in_position:
            return False

        if price > self.high_price:
            self.high_price = price
            return False

        drop_pct = ((self.high_price - price) / self.high_price) * 100
        if drop_pct >= self.trailing_threshold_pct:
            self.in_position = False
            self.high_price = None
            return True
        else:
            return False

def main():
    with open("config.json") as f:
        config = json.load(f)

    trailing_stop_pct = config["trailing_stop_pct"]
    entry_threshold = config["entry_threshold"]

    df = pd.read_csv("market_data_BTC.csv")

    exit_engine = ExitStrategy(trailing_threshold_pct=trailing_stop_pct)
    cumulative_profit = 0
    returns = []
    wins = 0
    losses = 0
    current_entry_price = None

    for _, row in df.iterrows():
        price = row["Price"]

        if not exit_engine.in_position:
            if price > entry_threshold:
                exit_engine.mark_entry(entry_price=price)
                current_entry_price = price
        else:
            if exit_engine.check_exit_signal(price):
                pnl = price - current_entry_price
                cumulative_profit += pnl
                returns.append(pnl)
                if pnl >= 0:
                    wins += 1
                else:
                    losses += 1
                current_entry_price = None

    total_trades = len(returns)
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    avg_return = (cumulative_profit / total_trades) if total_trades > 0 else 0

    print("\nStrategy Backtest Complete")
    print("----------------------------")
    print(f"Total Trades: {total_trades}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Average Return: {avg_return:.2f}")
    print(f"Cumulative Profit: {cumulative_profit:.2f}")

if __name__ == "__main__":
    main()
