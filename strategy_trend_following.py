import json
from datetime import datetime, timezone
from random import choice

def generate_trend_signals():
    timestamp = datetime.now(timezone.utc).isoformat()
    signals = []
    for symbol in ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]:
        signals.append({
            "symbol": symbol,
            "signal": choice(["buy", "sell"]),
            "confidence": 0.65
        })
    return {
        "timestamp": timestamp,
        "strategy": "trend_following",
        "signals": signals
    }

if __name__ == "__main__":
    print(json.dumps(generate_trend_signals(), indent=2))
