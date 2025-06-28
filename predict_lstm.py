#!/usr/bin/env python3

"""
predict_lstm.py
Loads trained LSTM models and generates predictions.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import os

# Parameters
SEQ_LENGTH = 24  # Must match training
PREDICT_ROWS = 1000  # Number of latest rows to predict

# Load data
X_df = pd.read_csv("./data/X_features.csv", index_col=0)
timestamps = X_df.index

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_df)

# Build sequences
X_seq = []
ts_seq = []
for i in range(SEQ_LENGTH, len(X_scaled)):
    X_seq.append(X_scaled[i-SEQ_LENGTH:i])
    ts_seq.append(timestamps[i])

X_seq = np.array(X_seq)
ts_seq = np.array(ts_seq)

# Use last N sequences
X_seq = X_seq[-PREDICT_ROWS:]
ts_seq = ts_seq[-PREDICT_ROWS:]

# Prepare predictions dataframe
preds_df = pd.DataFrame(index=ts_seq)

# Load models and predict
model_dir = "./data/lstm_models"
for filename in os.listdir(model_dir):
    if filename.endswith(".keras"):
        model_path = os.path.join(model_dir, filename)
        token_name = filename.replace("lstm_", "").replace(".keras", "")
        print(f"Predicting with model: {token_name}")

        model = tf.keras.models.load_model(model_path)
        preds = model.predict(X_seq, verbose=0)

        preds_df[token_name] = preds.flatten()

# Save predictions
preds_df.index.name = "timestamp"
preds_df.to_csv("./data/lstm_predictions.csv")

print("\n✅ Predictions saved to ./data/lstm_predictions.csv.")
