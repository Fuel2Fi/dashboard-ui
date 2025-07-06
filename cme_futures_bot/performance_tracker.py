import pandas as pd
import os

class PerformanceTracker:
    def __init__(self, log_file="performance_log.csv"):
        self.log_file = log_file
        if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
            df = pd.DataFrame(columns=[
                "Date",
                "Strategy",
                "Signal",
                "EntryPrice",
                "ExitPrice",
                "P&L"
            ])
            df.to_csv(log_file, index=False)

    def log_trade(self, date, strategy, signal, entry_price, exit_price=None):
        pnl = None
        if exit_price is not None and entry_price is not None:
            pnl = exit_price - entry_price if signal == "BUY" else entry_price - exit_price

        new_entry = pd.DataFrame([{
            "Date": str(date),
            "Strategy": str(strategy),
            "Signal": str(signal),
            "EntryPrice": float(entry_price) if entry_price is not None else None,
            "ExitPrice": float(exit_price) if exit_price is not None else None,
            "P&L": float(pnl) if pnl is not None else None
        }])

        try:
            if os.path.getsize(self.log_file) == 0:
                updated = new_entry
            else:
                existing = pd.read_csv(self.log_file)
                existing = existing.dropna(how="all")  # <--- This line ensures no all-NA rows

                expected_types = {
                    "Date": str,
                    "Strategy": str,
                    "Signal": str,
                    "EntryPrice": float,
                    "ExitPrice": float,
                    "P&L": float
                }
                for col, typ in expected_types.items():
                    if col in existing.columns:
                        existing[col] = existing[col].astype(typ)

                if existing.empty:
                    updated = new_entry
                else:
                    updated = pd.concat([existing, new_entry], ignore_index=True)

        except (pd.errors.EmptyDataError, FileNotFoundError):
            updated = new_entry

        updated.to_csv(self.log_file, index=False)

    def compute_stats(self):
        df = pd.read_csv(self.log_file)
        df = df.dropna(subset=["P&L"])

        total_trades = len(df)
        wins = df[df["P&L"] > 0]
        win_rate = len(wins) / total_trades * 100 if total_trades > 0 else 0
        avg_pnl = df["P&L"].mean() if total_trades > 0 else 0
        pnl_std = df["P&L"].std() if total_trades > 0 else 0
        sharpe = (avg_pnl / pnl_std) * (252 ** 0.5) if pnl_std > 0 else 0

        stats = {
            "Total Trades": total_trades,
            "Win Rate (%)": win_rate,
            "Average P&L": avg_pnl,
            "Sharpe Ratio": sharpe
        }
        return stats
