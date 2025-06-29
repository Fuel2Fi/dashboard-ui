#!/usr/bin/env bash

cd ~/Desktop/trading_bot

echo "========================================"
echo "🚀 Starting Full Auto-Trade Cycle: $(date)"
echo "========================================"

# 1. Run strategies
python3 strategy_breakout.py
python3 strategy_momentum.py
python3 strategy_trend_following.py
python3 strategy_volatility_expansion.py
python3 strategy_rsi_divergence.py
python3 strategy_ml_classifier.py

# 2. Run strategy switcher
python3 strategy_switcher.py

# 3. Execute trades based on switcher decisions
python3 auto_execute_switcher_trades.py

echo "✅ All tasks completed: $(date)"
