#!/usr/bin/env python3

"""
train_xgboost.py
Trains XGBoost regressors on Binance features and reports RMSE.
"""

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
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

# Create output dir
model_dir = "./data/xgboost_models"
os.makedirs(model_dir, exist_ok=True)

# Loop over each target column and train separate XGBoost model
for col in y.columns:
    print(f"\nTraining XGBoost for target: {col}")

    dtrain = xgb.DMatrix(X_train, label=y_train[col])
    dval = xgb.DMatrix(X_val, label=y_val[col])

    params = {
        "objective": "reg:squarederror",
        "max_depth": 6,
        "eta": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "seed": 42
    }

    model = xgb.train(
        params,
        dtrain,
        num_boost_round=500,
        evals=[(dtrain, "train"), (dval, "val")],
        early_stopping_rounds=20,
        verbose_eval=False
    )

    # Predict
    preds = model.predict(dval)
    mse = mean_squared_error(y_val[col], preds)
    rmse = np.sqrt(mse)
    stddev = y_val[col].std()

    print(f"✅ {col}: RMSE={rmse:.6f} (Target StdDev={stddev:.6f})")

    # Save model
    model_path = os.path.join(model_dir, f"xgboost_{col}.model")
    model.save_model(model_path)
    print(f"Model saved to {model_path}")

print("\n✅ All XGBoost models trained and saved.")
