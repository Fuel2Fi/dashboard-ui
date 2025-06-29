#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta

# Define strategy output files
strategy_files = [
    "./strategy_breakout_output.json",
    "./strategy_momentum_output.json",
    "./strategy_trend_following_output.json",
    "./strategy_volatility_expansion_output.json",
    "./strategy_rsi_divergence_output.json",
    "./strategy_ml_classifier_output.json",
    "./strategy_sentiment_output.json"
]

# Load all strategy outputs
strategies = []
for path in strategy_files:
    if os.path.exists(path):
        with open(path, "r") as f:
            strategies.append(json.load(f))
    else:
        print(f"⚠️ Missing strategy file: {path}")

# Tally votes per symbol
symbol_votes = {}

for strat in strategies:
    for s in strat["signals"]:
        sym = s["symbol"]
        vote = s["signal"]
        conf = s["confidence"]

        if sym not in symbol_votes:
            symbol_votes[sym] = {"buy": 0, "sell": 0, "hold": 0, "conf_sum": {"buy":0,"sell":0,"hold":0}}
        symbol_votes[sym][vote] += 1
        symbol_votes[sym]["conf_sum"][vote] += conf

# Decide per symbol: Require at least 2 votes and average confidence >0.65
decisions = []
for sym, votes in symbol_votes.items():
    decision = "hold"
    max_vote = 0
    avg_conf = 0.0
    for action in ["buy","sell","hold"]:
        if votes[action] > max_vote:
            max_vote = votes[action]
            avg_conf = votes["conf_sum"][action] / votes[action] if votes[action]>0 else 0.0
            decision = action
        elif votes[action] == max_vote and avg_conf < (votes["conf_sum"][action]/votes[action] if votes[action]>0 else 0.0):
            avg_conf = votes["conf_sum"][action]/votes[action]
            decision = action

    if max_vote < 2 or avg_conf < 0.65:
        decision = "hold"

    decisions.append({
        "symbol": sym,
        "decision": decision,
        "votes": votes,
        "avg_confidence": round(avg_conf,3)
    })

# Output
output = {
    "timestamp": datetime.utcnow().isoformat(),
    "method": "dynamic_switching",
    "decisions": decisions
}

print(json.dumps(output, indent=2))

with open("./strategy_switcher_output.json", "w") as f:
    json.dump(output, f, indent=2)
