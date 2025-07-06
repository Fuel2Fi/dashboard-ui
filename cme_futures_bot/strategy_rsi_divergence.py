import pandas as pd
import ta

def analyze(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple RSI divergence strategy:
    Buy when RSI crosses up from below 30 (oversold).
    Sell when RSI crosses down from above 70 (overbought).
    """
    df = df.copy()

    # RSI
    rsi_indicator = ta.momentum.RSIIndicator(
        close=df["Close"],
        window=14
    )
    df["RSI"] = rsi_indicator.rsi()

    signals = []
    prev_rsi = None

    for idx, row in df.iterrows():
        signal = "HOLD"

        if prev_rsi is not None:
            # Cross up from oversold
            if prev_rsi < 30 and row["RSI"] >= 30:
                signal = "BUY"
            # Cross down from overbought
            elif prev_rsi > 70 and row["RSI"] <= 70:
                signal = "SELL"

        signals.append(signal)
        prev_rsi = row["RSI"]

    df["Signal"] = signals
    return df
