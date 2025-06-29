#!/usr/bin/env python3
import json
from datetime import datetime
import random

# Simulated sentiment scores (in a real bot, you'd pull this from an API)
symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]
signals = []

for symbol in symbols:
    # Simulated sentiment: -1.0 (very negative) to +1.0 (very positive)
    sentiment_score = random.uniform(-1, 1)

    if sentiment_score > 0.3:
        signal = "buy"
        confidence = 0.7
    elif sentiment_score < -0.3:
        signal = "sell"
        confidence = 0.7
    else:
        signal = "hold"
        confidence = 0.6

    signals.append({
        "symbol": symbol,
        "signal": signal,
        "confidence": confidence,
        "sentiment_score": sentiment_score
    })

output = {
    "timestamp": datetime.utcnow().isoformat(),
    "strategy": "sentiment",
    "signals": signals
}

# Print and save
print(json.dumps(output, indent=2))
with open("./strategy_sentiment_output.json", "w") as f:
    json.dump(output, f, indent=2)
