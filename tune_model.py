#!/usr/bin/env python3

"""
tune_model.py
Performs hyperparameter tuning on Random Forest and reports MSE and RMSE.
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load features and targets
X = pd.read_csv("./data/X_features.csv", index_col=0)
y = pd.read_csv("./data/y_targets.csv", index_col=0)

# Align indices
X, y = X.align(y, join="inner", axis=0)

# Train/test split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Hyperparameter grid
param_grid = [
    {"n_estimators": 100, "max_depth": 10, "min_samples_leaf": 1},
    {"n_estimators": 300, "max_depth": 15, "min_samples_leaf": 1},
    {"n_estimators": 500, "max_depth": 20, "min_samples_leaf": 2},
    {"n_estimators": 700, "max_depth": 25, "min_samples_leaf": 3}
]

# Store results
results = []

# Loop through hyperparameter configurations
for params in param_grid:
    print(f"\nTraining with params: {params}")

    model = RandomForestRegressor(
        n_estimators=params["n_estimators"],
        max_depth=params["max_depth"],
        min_samples_leaf=params["min_samples_leaf"],
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

    mse_per_token = {}
    rmse_per_token = {}
    stddev_per_token = {}

    for idx, col in enumerate(y.columns):
        mse = mean_squared_error(y_val.iloc[:, idx], y_pred[:, idx])
        rmse = np.sqrt(mse)
        stddev = y_val.iloc[:, idx].std()
        mse_per_token[col] = mse
        rmse_per_token[col] = rmse
        stddev_per_token[col] = stddev

    results.append({
        "params": params,
        "mse": mse_per_token,
        "rmse": rmse_per_token
    })

    print("✅ Validation MSE and RMSE per token:")
    for token in y.columns:
        print(f"{token}: MSE={mse_per_token[token]:.6f}, RMSE={rmse_per_token[token]:.6f}, Target StdDev={stddev_per_token[token]:.6f}")

print("\n✅ Tuning complete.")
