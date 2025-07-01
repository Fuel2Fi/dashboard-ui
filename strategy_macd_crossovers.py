import json
from datetime import datetime
from random import choice

def generate_macd_signals():
    timestamp = datetime.now(datetime.UTC).isoformat()
    signals = []
    for symbol in ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]:
        signals.append({
            "symbol": symbol,
            "signal": choice(["buy", "sell"]),
            "confidence": 0.7
        })
    return {
        "timestamp": timestamp,
        "strategy": "macd_crossovers",
        "signals": signals
    }

if __name__ == "__main__":
    print(json.dumps(generate_macd_signals(), indent=2))
