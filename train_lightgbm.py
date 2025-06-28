#!/usr/bin/env python3

"""
train_lightgbm.py
Trains LightGBM regressors using scikit-learn API with callbacks.
"""

import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os

# Load data
X = pd.read_csv("./data/X_features.csv", index_col=0)
y = pd.read_csv("./data/y_targets.csv", index_col=0)

# Align indices
X, y = X.align(y, join="inner", axis=0)

# Train/test split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Create model directory
model_dir = "./data/lightgbm_models"
os.makedirs(model_dir, exist_ok=True)

# Loop through targets
for col in y.columns:
    print(f"\nTraining LightGBM for target: {col}")

    model = lgb.LGBMRegressor(
        n_estimators=1000,
        learning_rate=0.05,
        num_leaves=31,
        objective="regression",
        verbosity=-1
    )

    model.fit(
        X_train,
        y_train[col],
        eval_set=[(X_val, y_val[col])],
        callbacks=[
            lgb.early_stopping(stopping_rounds=20, verbose=False),
            lgb.log_evaluation(0)
        ]
    )

    preds = model.predict(X_val)
    mse = mean_squared_error(y_val[col], preds)
    rmse = np.sqrt(mse)
    stddev = y_val[col].std()

    print(f"✅ {col}: RMSE={rmse:.6f} (Target StdDev={stddev:.6f})")

    model_path = os.path.join(model_dir, f"lightgbm_{col}.txt")
    model.booster_.save_model(model_path)
    print(f"Model saved to {model_path}")

print("\n✅ All LightGBM models trained and saved.")
