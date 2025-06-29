#!/usr/bin/env python3
import pandas as pd
import ta

# Symbols to process
symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]

# List to hold all processed data
all_data = []

for symbol in symbols:
    # Load 4H OHLC
    df = pd.read_csv(f"./data_4h/{symbol}_4h_ohlc.csv")
    df["open_time"] = pd.to_datetime(df["open_time"])
    df = df.set_index("open_time")

    # Example: generate 8 simple features per symbol (expand as needed to match your model)
    df[f"{symbol}_rsi"] = ta.momentum.rsi(df["close"], window=14)
    df[f"{symbol}_ema"] = ta.trend.ema_indicator(df["close"], window=21)
    df[f"{symbol}_macd"] = ta.trend.macd_diff(df["close"])
    df[f"{symbol}_atr"] = ta.volatility.average_true_range(df["high"], df["low"], df["close"])
    df[f"{symbol}_roc"] = ta.momentum.roc(df["close"])
    df[f"{symbol}_stoch"] = ta.momentum.stoch_signal(df["high"], df["low"], df["close"])
    df[f"{symbol}_adx"] = ta.trend.adx(df["high"], df["low"], df["close"])
    df[f"{symbol}_volatility"] = ta.volatility.bollinger_hband(df["close"]) - ta.volatility.bollinger_lband(df["close"])

    # Keep only these columns
    feature_cols = [c for c in df.columns if symbol in c]
    df_features = df[feature_cols]

    all_data.append(df_features)

# Merge all features
df_all = pd.concat(all_data, axis=1).dropna()

# Save to CSV
df_all.to_csv("./data/X_features.csv")
print("✅ Generated and saved feature set: ./data/X_features.csv")
