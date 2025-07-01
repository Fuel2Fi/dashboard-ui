import json
from datetime import datetime, timezone

def generate_breakout_signals():
    timestamp = datetime.now(timezone.utc).isoformat()
    signals = []
    for symbol in ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]:
        signals.append({
            "symbol": symbol,
            "signal": "hold",
            "confidence": 0.75
        })
    return {
        "timestamp": timestamp,
        "strategy": "breakout",
        "signals": signals
    }

if __name__ == "__main__":
    print(json.dumps(generate_breakout_signals(), indent=2))
