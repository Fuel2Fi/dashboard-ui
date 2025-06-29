#!/usr/bin/env python3
import pandas as pd
import joblib
import json
from datetime import datetime

# Load trained model
model = joblib.load("./trained_model.joblib")

# Load latest features
df = pd.read_csv("./data/X_features.csv")

# Drop non-numeric columns (like timestamps)
numeric_df = df.select_dtypes(include=['number'])

# Get last row of numeric data
latest_row = numeric_df.iloc[-1].values.reshape(1, -1)

# Predict target return
pred_return = model.predict(latest_row)[0]

# Translate prediction to signal
if pred_return > 0.002:
    signal = "buy"
    confidence = 0.75
elif pred_return < -0.002:
    signal = "sell"
    confidence = 0.75
else:
    signal = "hold"
    confidence = 0.6

# Build output
output = {
    "timestamp": datetime.utcnow().isoformat(),
    "strategy": "ml_classifier",
    "signals": [
        {
            "symbol": "BTCUSDT",
            "signal": signal,
            "confidence": confidence
        }
    ]
}

# Print and save
print(json.dumps(output, indent=2))
with open("./strategy_ml_classifier_output.json", "w") as f:
    json.dump(output, f, indent=2)
