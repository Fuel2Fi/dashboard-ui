import json
from datetime import datetime, timezone
from random import choice

def generate_rsi_divergence_signals():
    timestamp = datetime.now(timezone.utc).isoformat()
    signals = []
    for symbol in ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]:
        signals.append({
            "symbol": symbol,
            "signal": choice(["buy", "hold"]),
            "confidence": 0.75
        })
    return {
        "timestamp": timestamp,
        "strategy": "rsi_divergence",
        "signals": signals
    }

if __name__ == "__main__":
    print(json.dumps(generate_rsi_divergence_signals(), indent=2))
