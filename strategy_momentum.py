import json
from datetime import datetime, timezone
from random import choice

def generate_momentum_signals():
    timestamp = datetime.now(timezone.utc).isoformat()
    signals = []
    for symbol in ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]:
        signals.append({
            "symbol": symbol,
            "signal": choice(["buy", "sell", "hold"]),
            "confidence": 0.7
        })
    return {
        "timestamp": timestamp,
        "strategy": "momentum",
        "signals": signals
    }

if __name__ == "__main__":
    print(json.dumps(generate_momentum_signals(), indent=2))
