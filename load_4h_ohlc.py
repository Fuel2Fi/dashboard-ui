#!/usr/bin/env python3
import os
import pandas as pd

def load_4h_ohlc(symbol):
    file_path = f"./data_4h/{symbol}_4h_ohlc.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing 4H OHLC file for {symbol}: {file_path}")
    df = pd.read_csv(file_path)
    df["open_time"] = pd.to_datetime(df["open_time"])
    return df
