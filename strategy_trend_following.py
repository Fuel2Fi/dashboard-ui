#!/usr/bin/env python3
import json
from datetime import datetime

timestamp = datetime.utcnow().isoformat()

signals = [
    {"symbol": "BTCUSDT", "signal": "sell", "confidence": 0.65},
    {"symbol": "ETHUSDT", "signal": "sell", "confidence": 0.65},
    {"symbol": "ADAUSDT", "signal": "buy", "confidence": 0.65},
    {"symbol": "BNBUSDT", "signal": "buy", "confidence": 0.65},
    {"symbol": "SOLUSDT", "signal": "buy", "confidence": 0.65},
]

output = {
    "timestamp": timestamp,
    "strategy": "trend_following",
    "signals": signals
}

print(json.dumps(output, indent=2))

with open("./strategy_trend_following_output.json", "w") as f:
    json.dump(output, f, indent=2)
