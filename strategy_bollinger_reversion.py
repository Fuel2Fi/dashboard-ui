#!/usr/bin/env python3
import pandas as pd
import json
from datetime import datetime

# Load 4H OHLC data
symbol_files = {
    "BTCUSDT": "./data_4h/BTCUSDT_4h_ohlc.csv",
    "ETHUSDT": "./data_4h/ETHUSDT_4h_ohlc.csv",
    "ADAUSDT": "./data_4h/ADAUSDT_4h_ohlc.csv",
    "BNBUSDT": "./data_4h/BNBUSDT_4h_ohlc.csv",
    "SOLUSDT": "./data_4h/SOLUSDT_4h_ohlc.csv",
}

signals = []

for symbol, file_path in symbol_files.items():
    df = pd.read_csv(file_path)
    df["open_time"] = pd.to_datetime(df["open_time"])

    # Calculate Bollinger Bands
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["std20"] = df["close"].rolling(window=20).std()
    df["upper"] = df["ma20"] + (2 * df["std20"])
    df["lower"] = df["ma20"] - (2 * df["std20"])

    last_row = df.iloc[-1]
    price = last_row["close"]

    # Signal logic
    if price <= last_row["lower"]:
        signal = "buy"
        confidence = 0.7
    elif price >= last_row["upper"]:
        signal = "sell"
        confidence = 0.7
    else:
        signal = "hold"
        confidence = 0.6

    signals.append({
        "symbol": symbol,
        "signal": signal,
        "confidence": confidence
    })

output = {
    "timestamp": datetime.utcnow().isoformat(),
    "strategy": "bollinger_reversion",
    "signals": signals
}

# Print and save
print(json.dumps(output, indent=2))
with open("./strategy_bollinger_reversion_output.json", "w") as f:
    json.dump(output, f, indent=2)
