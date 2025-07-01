import json
from datetime import datetime, timezone
from random import choice, uniform

def generate_volatility_signals():
    timestamp = datetime.now(timezone.utc).isoformat()
    signals = []
    for symbol in ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]:
        signals.append({
            "symbol": symbol,
            "signal": choice(["buy", "sell", "hold"]),
            "confidence": round(uniform(0.6, 0.8), 2)
        })
    return {
        "timestamp": timestamp,
        "strategy": "volatility_expansion",
        "signals": signals
    }

if __name__ == "__main__":
    print(json.dumps(generate_volatility_signals(), indent=2))
