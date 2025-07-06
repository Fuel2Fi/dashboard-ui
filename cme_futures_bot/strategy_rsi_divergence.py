import pandas as pd
import ta

def analyze(df: pd.DataFrame) -> pd.DataFrame:
    """
    RSI Divergence strategy:
    - Buy if RSI < 30 (oversold).
    - Sell if RSI > 70 (overbought).
    - Otherwise hold.
    """
    df = df.copy()

    # RSI
    rsi = ta.momentum.RSIIndicator(close=df["Close"], window=14)
    df["RSI"] = rsi.rsi()

    signals = []
    for idx, row in df.iterrows():
        signal = "HOLD"
        if pd.notnull(row["RSI"]):
            if row["RSI"] < 30:
                signal = "BUY"
            elif row["RSI"] > 70:
                signal = "SELL"
        signals.append(signal)

    df["Signal"] = signals
    return df
