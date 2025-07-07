import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

def run_backtest(df, trailing_stop_pct):
    exit_engine = ExitStrategy(trailing_threshold_pct=trailing_stop_pct)
    cumulative_profit = 0
    equity_curve = []
    returns = []
    current_entry_price = None

    log = []

    for _, row in df.iterrows():
        price = row["Price"]
        date = row["Date"]

        if not exit_engine.in_position:
            if price > 1000:
                exit_engine.mark_entry(entry_price=price)
                current_entry_price = price
                log.append((date, price, "Entry"))
        else:
            if exit_engine.check_exit_signal(price):
                pnl = price - current_entry_price
                cumulative_profit += pnl
                returns.append(pnl)
                equity_curve.append(cumulative_profit)
                log.append((date, price, f"Exit (PnL: {pnl})"))
                current_entry_price = None
            else:
                equity_curve.append(cumulative_profit)

    results = {
        "Total Trades": len(returns),
        "Cumulative Profit": cumulative_profit,
        "Win Rate": (np.sum(np.array(returns) > 0) / len(returns) * 100) if returns else 0,
        "Equity Curve": equity_curve,
        "Log": log
    }
    return results

def main():
    st.title("Trading Strategy Dashboard")

    uploaded_file = st.file_uploader("Upload your market data CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df["Date"] = pd.to_datetime(df["Date"])

        trailing_stop = st.slider("Trailing Stop (%)", min_value=1, max_value=20, value=5, step=1)

        results = run_backtest(df, trailing_stop)

        st.subheader("Performance Metrics")
        st.write(f"Total Trades: {results['Total Trades']}")
        st.write(f"Cumulative Profit: {results['Cumulative Profit']}")
        st.write(f"Win Rate: {results['Win Rate']:.2f}%")

        st.subheader("Equity Curve")
        fig, ax = plt.subplots()
        ax.plot(results["Equity Curve"], color="blue")
        ax.set_xlabel("Trades")
        ax.set_ylabel("Cumulative Profit")
        st.pyplot(fig)

        st.subheader("Trade Log")
        log_df = pd.DataFrame(results["Log"], columns=["Date", "Price", "Action"])
        st.dataframe(log_df)

if __name__ == "__main__":
    main()
