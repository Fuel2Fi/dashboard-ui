import json
from datetime import datetime, timezone
import joblib
import numpy as np

model = joblib.load("./trained_model.joblib")

def generate_ml_signals():
    timestamp = datetime.now(timezone.utc).isoformat()
    # Generate random data with 40 features to match model training
    predictions = model.predict(np.random.rand(5, 40))
    signals = []
    for symbol, pred in zip(["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"], predictions):
        signals.append({
            "symbol": symbol,
            "signal": "buy" if pred > 0.5 else "sell",
            "confidence": round(float(pred), 2)
        })
    return {
        "timestamp": timestamp,
        "strategy": "ml_classifier",
        "signals": signals
    }

if __name__ == "__main__":
    print(json.dumps(generate_ml_signals(), indent=2))
