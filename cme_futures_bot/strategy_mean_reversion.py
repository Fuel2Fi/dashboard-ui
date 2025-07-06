import pandas as pd
import ta

def analyze(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mean-reversion strategy using Bollinger Bands.
    Buy when price closes below lower band.
    Sell when price closes above upper band.
    """
    df = df.copy()

    bb = ta.volatility.BollingerBands(
        close=df["Close"],
        window=20,
        window_dev=2
    )

    df["bb_high"] = bb.bollinger_hband()
    df["bb_low"] = bb.bollinger_lband()

    signals = []
    for idx, row in df.iterrows():
        signal = "HOLD"
        if pd.notnull(row["bb_high"]) and pd.notnull(row["bb_low"]):
            if row["Close"] < row["bb_low"]:
                signal = "BUY"
            elif row["Close"] > row["bb_high"]:
                signal = "SELL"
        signals.append(signal)

    df["Signal"] = signals
    return df
