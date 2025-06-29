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

    # Calculate MACD components
    df["ema12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["ema26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = df["ema12"] - df["ema26"]
    df["signal_line"] = df["macd"].ewm(span=9, adjust=False).mean()

    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # Detect crossover
    if prev_row["macd"] < prev_row["signal_line"] and last_row["macd"] > last_row["signal_line"]:
        signal = "buy"
        confidence = 0.75
    elif prev_row["macd"] > prev_row["signal_line"] and last_row["macd"] < last_row["signal_line"]:
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
    "timestamp": datetime.utcnow().isoformat(),
    "strategy": "macd_crossovers",
    "signals": signals
}

# Print and save
print(json.dumps(output, indent=2))
with open("./strategy_macd_crossovers_output.json", "w") as f:
    json.dump(output, f, indent=2)
