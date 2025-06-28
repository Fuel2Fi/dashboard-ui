#!/usr/bin/env python3
import pandas as pd

# Load predictions
df = pd.read_csv('./data/lstm_predictions.csv', parse_dates=['timestamp'])

# Thresholds
threshold = 0.005

signals = df.copy()
for col in df.columns[1:]:
    signals[col] = df[col].apply(
        lambda x: 'BUY' if x > threshold else ('SELL' if x < -threshold else 'HOLD')
    )

signals.to_csv('./data/lstm_trade_signals.csv', index=False)
print("✅ Trade signals saved to ./data/lstm_trade_signals.csv.")
