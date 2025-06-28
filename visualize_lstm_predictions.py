#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

# Load predictions
df = pd.read_csv('./data/lstm_predictions.csv', parse_dates=['timestamp'])
df.set_index('timestamp', inplace=True)

# Create plots for each asset
for column in df.columns:
    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df[column], marker='o')
    plt.title(f'Predicted Returns - {column}')
    plt.xlabel('Timestamp')
    plt.ylabel('Predicted Return')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'./data/prediction_{column}.png')
    plt.close()

print("✅ Visualizations saved to ./data/ as PNG files.")
