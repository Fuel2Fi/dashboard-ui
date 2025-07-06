import pandas as pd

def analyze(df: pd.DataFrame) -> pd.DataFrame:
    """
    Breakout strategy:
    - Buy when price closes above prior 20-day high.
    - Sell when price closes below prior 20-day low.
    - Otherwise hold.
    """
    df = df.copy()
    df["20d_high"] = df["High"].rolling(window=20).max().shift(1)
    df["20d_low"] = df["Low"].rolling(window=20).min().shift(1)

    signals = []
    for idx, row in df.iterrows():
        signal = "HOLD"
        if pd.notnull(row["20d_high"]) and row["Close"] > row["20d_high"]:
            signal = "BUY"
        elif pd.notnull(row["20d_low"]) and row["Close"] < row["20d_low"]:
            signal = "SELL"
        signals.append(signal)

    df["Signal"] = signals
    return df
