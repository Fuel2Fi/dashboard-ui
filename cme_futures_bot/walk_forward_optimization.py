import pandas as pd

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

def backtest(df, trailing_stop_pct):
    exit_engine = ExitStrategy(trailing_threshold_pct=trailing_stop_pct)
    cumulative_profit = 0
    wins = 0
    losses = 0
    total_trades = 0
    current_entry_price = None

    for _, row in df.iterrows():
        price = row["Price"]
        if not exit_engine.in_position:
            if price > 1000:
                exit_engine.mark_entry(entry_price=price)
                current_entry_price = price
        else:
            if exit_engine.check_exit_signal(price):
                pnl = price - current_entry_price
                cumulative_profit += pnl
                total_trades += 1
                if pnl >= 0:
                    wins += 1
                else:
                    losses += 1
                current_entry_price = None

    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    avg_return = (cumulative_profit / total_trades) if total_trades > 0 else 0
    return {
        "TotalTrades": total_trades,
        "Wins": wins,
        "Losses": losses,
        "WinRatePct": round(win_rate, 2),
        "AverageReturn": round(avg_return, 2),
        "CumulativeProfit": round(cumulative_profit, 2)
    }

def main():
    df = pd.read_csv("market_data_BTC.csv")  # Use any asset for example
    split_idx = int(len(df) * 0.7)
    in_sample = df.iloc[:split_idx]
    out_sample = df.iloc[split_idx:]

    thresholds = [3,5,7,10]
    print("🎯 In-Sample Optimization Results:")
    best_threshold = None
    best_profit = float('-inf')
    for t in thresholds:
        result = backtest(in_sample, t)
        print(f"TrailingStop {t}% -> Profit: {result['CumulativeProfit']}")
        if result["CumulativeProfit"] > best_profit:
            best_profit = result["CumulativeProfit"]
            best_threshold = t

    print(f"\n✅ Best trailing stop: {best_threshold}% (Profit: {best_profit})")

    print("\n🎯 Out-of-Sample Evaluation:")
    result_out = backtest(out_sample, best_threshold)
    print(f"TrailingStop {best_threshold}% -> Profit: {result_out['CumulativeProfit']}, WinRate: {result_out['WinRatePct']}%")

if __name__ == "__main__":
    main()
