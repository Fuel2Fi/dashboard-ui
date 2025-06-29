#!/usr/bin/env python3
import json
import pandas as pd
from datetime import datetime

timestamp = datetime.utcnow().isoformat()

symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]

signals = []

for symbol in symbols:
    # Load 4H OHLC data
    df = pd.read_csv(f"./data_4h/{symbol}_4h_ohlc.csv")
    df["open_time"] = pd.to_datetime(df["open_time"])
    df.set_index("open_time", inplace=True)

    # Compute RSI (14)
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    last_rsi = df["rsi"].iloc[-1]
    prev_rsi = df["rsi"].iloc[-2]
    last_price = df["close"].iloc[-1]
    prev_price = df["close"].iloc[-2]

    # Detect divergence
    if last_rsi > prev_rsi and last_price < prev_price:
        signal = "buy"
        confidence = 0.75
    elif last_rsi < prev_rsi and last_price > prev_price:
        signal = "sell"
        confidence = 0.75
    else:
        signal = "hold"
        confidence = 0.6

    signals.append({
        "symbol": symbol,
        "signal": signal,
        "confidence": confidence
    })

output = {
    "timestamp": timestamp,
    "strategy": "rsi_divergence",
    "signals": signals
}

print(json.dumps(output, indent=2))

with open("./strategy_rsi_divergence_output.json", "w") as f:
    json.dump(output, f, indent=2)
