#!/usr/bin/env python3
import pandas as pd
import json
from datetime import datetime

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr

# Load 4H OHLC data
symbol_files = {
    "BTCUSDT": "./data_4h/BTCUSDT_4h_ohlc.csv",
    "ETHUSDT": "./data_4h/ETHUSDT_4h_ohlc.csv",
    "ADAUSDT": "./data_4h/ADAUSDT_4h_ohlc.csv",
    "BNBUSDT": "./data_4h/BNBUSDT_4h_ohlc.csv",
    "SOLUSDT": "./data_4h/SOLUSDT_4h_ohlc.csv"
}

signals = []

for symbol, filepath in symbol_files.items():
    df = pd.read_csv(filepath)
    df['open_time'] = pd.to_datetime(df['open_time'])
    df.sort_values('open_time', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Calculate ATR
    df['ATR'] = calculate_atr(df)

    # Use last completed candle
    last_row = df.iloc[-2]
    atr_last = last_row['ATR']
    atr_mean = df['ATR'][-21:-1].mean()  # prior 20

    # Determine if volatility expansion
    if atr_last > 1.5 * atr_mean:
        # Decide direction
        if last_row['close'] > last_row['open']:
            signal = 'buy'
        else:
            signal = 'sell'
    else:
        signal = 'hold'

    signals.append({
        "symbol": symbol,
        "signal": signal,
        "confidence": 0.8 if signal != 'hold' else 0.6
    })

output = {
    "timestamp": datetime.utcnow().isoformat(),
    "strategy": "volatility_expansion",
    "signals": signals
}

print(json.dumps(output, indent=2))

# Save to file
with open("./strategy_volatility_expansion_output.json", "w") as f:
    json.dump(output, f, indent=2)
