#!/usr/bin/env python3

"""
train_lstm.py
Trains an LSTM model for each target using Keras.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os

# Parameters
SEQ_LENGTH = 24  # 24 hours history
BATCH_SIZE = 32
EPOCHS = 20

# Load data
X_df = pd.read_csv("./data/X_features.csv", index_col=0)
y_df = pd.read_csv("./data/y_targets.csv", index_col=0)

# Align indices
X_df, y_df = X_df.align(y_df, join="inner", axis=0)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_df)

# Convert to numpy
X = X_scaled
y = y_df.values

# Build sequences
X_seq = []
y_seq = []
for i in range(SEQ_LENGTH, len(X)):
    X_seq.append(X[i-SEQ_LENGTH:i])
    y_seq.append(y[i])

X_seq = np.array(X_seq)
y_seq = np.array(y_seq)

# Train/test split
split_idx = int(len(X_seq)*0.8)
X_train, X_val = X_seq[:split_idx], X_seq[split_idx:]
y_train, y_val = y_seq[:split_idx], y_seq[split_idx:]

# Create model directory
model_dir = "./data/lstm_models"
os.makedirs(model_dir, exist_ok=True)

# Loop through targets
for col_idx, col_name in enumerate(y_df.columns):
    print(f"\nTraining LSTM for target: {col_name}")

    # Build LSTM model
    model = keras.Sequential([
        layers.Input(shape=(SEQ_LENGTH, X.shape[1])),
        layers.LSTM(64, return_sequences=True),
        layers.LSTM(32),
        layers.Dense(1)
    ])

    model.compile(
        loss="mse",
        optimizer="adam"
    )

    # Train
    history = model.fit(
        X_train,
        y_train[:, col_idx],
        validation_data=(X_val, y_val[:, col_idx]),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1
    )

    # Predict
    preds = model.predict(X_val)
    mse = mean_squared_error(y_val[:, col_idx], preds)
    rmse = np.sqrt(mse)
    stddev = np.std(y_val[:, col_idx])

    print(f"✅ {col_name}: RMSE={rmse:.6f} (Target StdDev={stddev:.6f})")

    # Save model with .keras extension
    model_path = os.path.join(model_dir, f"lstm_{col_name}.keras")
    model.save(model_path)
    print(f"Model saved to {model_path}")

print("\n✅ All LSTM models trained and saved.")
