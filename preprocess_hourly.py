#!/usr/bin/env python3

"""
preprocess_hourly.py
Processes Binance hourly OHLC data with advanced technical indicators.
"""

import pandas as pd
import pandas_ta as ta
import os

# Input directory
input_dir = "./data_hourly"

# Tokens
tokens = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT"]

feature_dfs = []

for token in tokens:
    file_path = os.path.join(input_dir, f"{token}_hourly_ohlc.csv")
    print(f"Processing {file_path}...")
    df = pd.read_csv(file_path, parse_dates=["open_time"], index_col="open_time")

    # Hourly return
    df["return"] = df["close"].pct_change()

    # Moving averages
    df["ma_7"] = df["close"].rolling(7).mean()
    df["ma_14"] = df["close"].rolling(14).mean()

    # Volatility
    df["volatility_30"] = df["return"].rolling(30).std()

    # Z-Score
    df["zscore_30"] = (df["close"] - df["close"].rolling(30).mean()) / df["close"].rolling(30).std()

    # RSI
    df["rsi_14"] = ta.rsi(df["close"], length=14)

    # MACD
    macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
    df["macd"] = macd["MACD_12_26_9"]
    df["macd_signal"] = macd["MACDs_12_26_9"]
    df["macd_diff"] = macd["MACDh_12_26_9"]

    # Bollinger Band Width
    bbands = ta.bbands(df["close"], length=20)
    df["bb_width"] = bbands["BBU_20_2.0"] - bbands["BBL_20_2.0"]

    # Lagged Returns
    df["return_lag1"] = df["return"].shift(1)
    df["return_lag2"] = df["return"].shift(2)
    df["return_lag3"] = df["return"].shift(3)

    # Forward target return
    df["target_return"] = df["return"].shift(-1)

    # Rename columns
    df = df.rename(columns={col: f"{token}_{col}" for col in df.columns})

    feature_dfs.append(df)

# Merge on timestamp
merged_df = pd.concat(feature_dfs, axis=1, join="inner")

# Drop NaNs
merged_df = merged_df.dropna()

# Split
X = merged_df.drop(columns=[col for col in merged_df.columns if col.endswith("target_return")])
y = merged_df[[col for col in merged_df.columns if col.endswith("target_return")]]

# Save
X.to_csv("./data/X_features.csv")
y.to_csv("./data/y_targets.csv")

print("\n✅ Hourly preprocessing complete. Features saved to ./data/X_features.csv, targets saved to ./data/y_targets.csv.")
