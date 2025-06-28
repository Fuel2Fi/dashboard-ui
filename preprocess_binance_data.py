#!/usr/bin/env python3

"""
preprocess_binance_data.py
Processes Binance daily OHLC data to create features and target datasets.
"""

import pandas as pd
import os

# Input directory
input_dir = "./data"

# Tokens
tokens = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT"]

feature_dfs = []

for token in tokens:
    file_path = os.path.join(input_dir, f"{token}_daily_ohlc.csv")
    print(f"Processing {file_path}...")
    df = pd.read_csv(file_path, parse_dates=["open_time"], index_col="open_time")

    # Calculate daily return
    df["return"] = df["close"].pct_change()

    # Calculate moving averages
    df["ma_7"] = df["close"].rolling(7).mean()
    df["ma_14"] = df["close"].rolling(14).mean()

    # Calculate rolling volatility (std dev)
    df["volatility_30"] = df["return"].rolling(30).std()

    # Rolling z-score of close price
    df["zscore_30"] = (df["close"] - df["close"].rolling(30).mean()) / df["close"].rolling(30).std()

    # Forward shift return as target
    df["target_return"] = df["return"].shift(-1)

    # Rename columns
    df = df.rename(columns={
        "close": f"{token}_close",
        "return": f"{token}_return",
        "ma_7": f"{token}_ma_7",
        "ma_14": f"{token}_ma_14",
        "volatility_30": f"{token}_volatility_30",
        "zscore_30": f"{token}_zscore_30",
        "target_return": f"{token}_target_return"
    })

    # Keep only the engineered columns
    df = df[[
        f"{token}_close",
        f"{token}_return",
        f"{token}_ma_7",
        f"{token}_ma_14",
        f"{token}_volatility_30",
        f"{token}_zscore_30",
        f"{token}_target_return"
    ]]

    feature_dfs.append(df)

# Merge all tokens on timestamp
merged_df = pd.concat(feature_dfs, axis=1, join="inner")

# Drop rows with any NaNs
merged_df = merged_df.dropna()

# Split into features (X) and target (y)
X = merged_df.drop(columns=[col for col in merged_df.columns if col.endswith("target_return")])
y = merged_df[[col for col in merged_df.columns if col.endswith("target_return")]]

# Save to CSV
X.to_csv("./data/X_features.csv")
y.to_csv("./data/y_targets.csv")

print(f"✅ Preprocessing complete. Features saved to ./data/X_features.csv, targets saved to ./data/y_targets.csv.")
