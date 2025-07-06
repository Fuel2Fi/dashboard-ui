import pandas as pd

def analyze(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple breakout strategy:
    Buy when close breaks above the prior 20-day high.
    Sell when close breaks below the prior 20-day low.
    """
    df = df.copy()
    df["20d_high"] = df["High"].rolling(window=20).max()
    df["20d_low"] = df["Low"].rolling(window=20).min()

    signals = []
    for idx, row in df.iterrows():
        signal = "HOLD"
        if row["Close"] > row["20d_high"]:
            signal = "BUY"
        elif row["Close"] < row["20d_low"]:
            signal = "SELL"
        signals.append(signal)

    df["Signal"] = signals
    return df
