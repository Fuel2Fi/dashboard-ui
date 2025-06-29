#!/usr/bin/env python3
import json
from datetime import datetime

timestamp = datetime.utcnow().isoformat()

signals = [
    {"symbol": "BTCUSDT", "signal": "sell", "confidence": 0.7},
    {"symbol": "ETHUSDT", "signal": "hold", "confidence": 0.7},
    {"symbol": "ADAUSDT", "signal": "hold", "confidence": 0.7},
    {"symbol": "BNBUSDT", "signal": "buy", "confidence": 0.7},
    {"symbol": "SOLUSDT", "signal": "hold", "confidence": 0.7},
]

output = {
    "timestamp": timestamp,
    "strategy": "momentum",
    "signals": signals
}

print(json.dumps(output, indent=2))

with open("./strategy_momentum_output.json", "w") as f:
    json.dump(output, f, indent=2)
