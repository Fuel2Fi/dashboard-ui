import json
from datetime import datetime
from random import choice

def generate_bollinger_signals():
    timestamp = datetime.now(datetime.UTC).isoformat()
    signals = []
    for symbol in ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]:
        signals.append({
            "symbol": symbol,
            "signal": choice(["buy", "sell", "hold"]),
            "confidence": 0.7
        })
    return {
        "timestamp": timestamp,
        "strategy": "bollinger_reversion",
        "signals": signals
    }

if __name__ == "__main__":
    print(json.dumps(generate_bollinger_signals(), indent=2))
