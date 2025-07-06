import pandas as pd

def analyze(df: pd.DataFrame) -> pd.DataFrame:
    """
    Minimal placeholder mean-reversion strategy.
    Always returns HOLD signals.
    """
    df = df.copy()
    df["Signal"] = "HOLD"
    return df
