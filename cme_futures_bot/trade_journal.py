import pandas as pd

class ExitStrategy:
    def __init__(self, trailing_threshold_pct):
        self.trailing_threshold_pct = trailing_threshold_pct
        self.high_price = None
        self.in_position = False

    def mark_entry(self, entry_price, entry_date):
        self.in_position = True
        self.high_price = entry_price
        self.entry_date = entry_date
        self.entry_price = entry_price

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
    df = pd.read_csv("market_data_BTC.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    exit_engine = ExitStrategy(trailing_threshold_pct=5)
    trade_records = []

    for _, row in df.iterrows():
        price = row["Price"]
        date = row["Date"]

        if not exit_engine.in_position:
            if price > 1000:
                exit_engine.mark_entry(entry_price=price, entry_date=date)
        else:
            if exit_engine.check_exit_signal(price):
                pnl = price - exit_engine.entry_price
                trade_records.append({
                    "EntryDate": exit_engine.entry_date,
                    "EntryPrice": exit_engine.entry_price,
                    "ExitDate": date,
                    "ExitPrice": price,
                    "PnL": pnl
                })

    if trade_records:
        trades_df = pd.DataFrame(trade_records)
        trades_df.to_csv("trade_journal.csv", index=False)
        print("✅ Trade journal saved to trade_journal.csv")
    else:
        print("⚠️ No trades executed. Journal not created.")

if __name__ == "__main__":
    main()
