#!/usr/bin/env python3
import json
from datetime import datetime

def load_strategy_signals(file_path):
    with open(file_path, "r") as f:
        return json.load(f)["signals"]

# Load all strategy outputs
breakout_signals = load_strategy_signals("./strategy_breakout_output.json")
momentum_signals = load_strategy_signals("./strategy_momentum_output.json")
trend_signals = load_strategy_signals("./strategy_trend_following_output.json")
volatility_signals = load_strategy_signals("./strategy_volatility_expansion_output.json")
rsi_signals = load_strategy_signals("./strategy_rsi_divergence_output.json")
ml_signals = load_strategy_signals("./strategy_ml_classifier_output.json")

symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"]

decisions = []

for symbol in symbols:
    votes = {"buy": 0, "sell": 0, "hold": 0}

    for strategy in [breakout_signals, momentum_signals, trend_signals, volatility_signals, rsi_signals, ml_signals]:
        for s in strategy:
            if s["symbol"] == symbol:
                votes[s["signal"]] += 1

    # Determine consensus with tie-breaker rules
    max_votes = max(votes.values())
    top_signals = [k for k, v in votes.items() if v == max_votes]

    if len(top_signals) == 1:
        consensus = top_signals[0]
    else:
        # Tie-breaker: prefer HOLD if tied
        if "hold" in top_signals:
            consensus = "hold"
        else:
            consensus = "hold"  # ultimate fallback

    decisions.append({
        "symbol": symbol,
        "consensus_signal": consensus,
        "vote_breakdown": votes
    })

output = {
    "timestamp": datetime.utcnow().isoformat(),
    "method": "majority_vote_with_tiebreak",
    "decisions": decisions
}

print(json.dumps(output, indent=2))

with open("./strategy_consensus_output.json", "w") as f:
    json.dump(output, f, indent=2)
