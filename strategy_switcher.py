import json
from datetime import datetime, timezone

def switch_strategies(all_signals):
    timestamp = datetime.now(timezone.utc).isoformat()
    decisions = []
    for symbol in ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]:
        votes = {"buy": 0, "sell": 0, "hold": 0, "conf_sum": {"buy":0, "sell":0, "hold":0}}
        for strategy in all_signals:
            for s in strategy["signals"]:
                if s["symbol"] == symbol:
                    votes[s["signal"]] += 1
                    votes["conf_sum"][s["signal"]] += s["confidence"]
        avg_conf = round(sum(votes["conf_sum"].values()) / 3, 3)
        decision = max(["buy","sell","hold"], key=lambda k: votes[k])
        decisions.append({
            "symbol": symbol,
            "decision": decision,
            "votes": votes,
            "avg_confidence": avg_conf
        })
    return {
        "timestamp": timestamp,
        "method": "dynamic_switching",
        "decisions": decisions
    }

if __name__ == "__main__":
    example_signals = []
    print(json.dumps(switch_strategies(example_signals), indent=2))
