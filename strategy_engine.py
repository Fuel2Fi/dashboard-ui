#!/usr/bin/env python3
import pandas as pd
import numpy as np
from load_4h_ohlc import load_4h_ohlc

def calculate_indicators(df):
    # Simple moving average example
    df["sma_10"] = df["close"].rolling(window=10).mean()
    df["sma_50"] = df["close"].rolling(window=50).mean()
    # RSI example
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi_14"] = 100 - (100 / (1 + rs))
    return df

def generate_signals(df):
    last = df.iloc[-1]
    if last["sma_10"] > last["sma_50"]:
        if last["rsi_14"] < 30:
            return "buy"
        else:
            return "hold"
    elif last["sma_10"] < last["sma_50"]:
        if last["rsi_14"] > 70:
            return "sell"
        else:
            return "hold"
    else:
        return "hold"

def select_strategy():
    # You could build more sophisticated selection here
    return "mean_reversion"

if __name__ == "__main__":
    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]
    actions = []

    for symbol in symbols:
        df = load_4h_ohlc(symbol)
        df = calculate_indicators(df)
        signal = generate_signals(df)

        action = {
            "symbol": symbol,
            "signal": signal,
            "action": (
                "open_long" if signal == "buy"
                else "open_short" if signal == "sell"
                else "hold"
            )
        }
        actions.append(action)

    strategy = select_strategy()

    output = {
        "timestamp": pd.Timestamp.utcnow().isoformat(),
        "strategy": strategy,
        "actions": actions
    }

    import json
    print(json.dumps(output, indent=2))
