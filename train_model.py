#!/usr/bin/env python3

"""
train_model.py
Trains a Random Forest model on Binance preprocessed data and reports MSE.
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Load features and targets
X = pd.read_csv("./data/X_features.csv", index_col=0)
y = pd.read_csv("./data/y_targets.csv", index_col=0)

# Align indices just in case
X, y = X.align(y, join="inner", axis=0)

# Train/test split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Train Random Forest
print("Training Random Forest...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_val)

# Compute MSE per token
mse_per_token = {}
for idx, col in enumerate(y.columns):
    mse = mean_squared_error(y_val.iloc[:, idx], y_pred[:, idx])
    mse_per_token[col] = mse

# Report results
print("\n✅ Validation MSE per token:")
for token, mse in mse_per_token.items():
    print(f"{token}: {mse:.6f}")

# Save model
joblib.dump(model, "./data/random_forest_model.pkl")
print("\n✅ Model saved to ./data/random_forest_model.pkl.")
