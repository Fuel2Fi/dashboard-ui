import pandas as pd
import numpy as np

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

def compute_drawdown(equity_curve):
    roll_max = equity_curve.cummax()
    drawdown = (equity_curve - roll_max)
    max_drawdown = drawdown.min()
    return max_drawdown

def main():
    df = pd.read_csv("market_data_BTC.csv")
    exit_engine = ExitStrategy(trailing_threshold_pct=5)
    cumulative_profit = 0
    returns = []
    equity_curve = []
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
                returns.append(pnl)
                equity_curve.append(cumulative_profit)
                current_entry_price = None

    if not returns:
        print("⚠️ No trades executed. Metrics cannot be calculated.")
        return

    # Convert to numpy for calculations
    returns = np.array(returns)
    equity_curve = pd.Series(equity_curve)

    sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(len(returns)) if np.std(returns) > 0 else 0
    max_drawdown = compute_drawdown(equity_curve)
    gross_profit = np.sum(returns[returns > 0])
    gross_loss = abs(np.sum(returns[returns < 0]))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else np.inf
    expectancy = np.mean(returns)

    print("\n🎯 Risk-Adjusted Metrics")
    print("-----------------------------")
    print(f"Total Trades: {len(returns)}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2f}")
    print(f"Profit Factor: {profit_factor:.2f}")
    print(f"Expectancy: {expectancy:.2f}")
    print(f"Cumulative Profit: {cumulative_profit:.2f}")

if __name__ == "__main__":
    main()
