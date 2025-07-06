import pandas as pd
import ta

def analyze(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trend-following strategy:
    - Buy when fast MA > slow MA and ADX > 25.
    - Sell when fast MA < slow MA and ADX > 25.
    - Otherwise hold.
    """
    df = df.copy()

    # Moving Averages
    df["fast_ma"] = df["Close"].rolling(window=10).mean()
    df["slow_ma"] = df["Close"].rolling(window=30).mean()

    # ADX Indicator
    adx_indicator = ta.trend.ADXIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )
    df["ADX"] = adx_indicator.adx()

    signals = []
    for idx, row in df.iterrows():
        signal = "HOLD"
        if pd.notnull(row["fast_ma"]) and pd.notnull(row["slow_ma"]) and pd.notnull(row["ADX"]):
            if row["fast_ma"] > row["slow_ma"] and row["ADX"] > 25:
                signal = "BUY"
            elif row["fast_ma"] < row["slow_ma"] and row["ADX"] > 25:
                signal = "SELL"
        signals.append(signal)

    df["Signal"] = signals
    return df
