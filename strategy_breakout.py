#!/usr/bin/env python3
import json
from datetime import datetime

timestamp = datetime.utcnow().isoformat()

signals = []
symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]

for symbol in symbols:
    signals.append({
        "symbol": symbol,
        "signal": "hold",
        "confidence": 0.75
    })

output = {
    "timestamp": timestamp,
    "strategy": "breakout",
    "signals": signals
}

# Print to console
print(json.dumps(output, indent=2))

# Save to file
with open("./strategy_breakout_output.json", "w") as f:
    json.dump(output, f, indent=2)
