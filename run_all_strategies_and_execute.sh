#!/bin/bash

echo "🚀 Running all strategies and auto-executor..."

# Strategy Scripts
/usr/bin/python3 /Users/damonholland777/Desktop/trading_bot/strategy_breakout.py
/usr/bin/python3 /Users/damonholland777/Desktop/trading_bot/strategy_momentum.py
/usr/bin/python3 /Users/damonholland777/Desktop/trading_bot/strategy_trend_following.py
/usr/bin/python3 /Users/damonholland777/Desktop/trading_bot/strategy_volatility_expansion.py
/usr/bin/python3 /Users/damonholland777/Desktop/trading_bot/strategy_rsi_divergence.py
/usr/bin/python3 /Users/damonholland777/Desktop/trading_bot/strategy_ml_classifier.py

# Consensus Engine
/usr/bin/python3 /Users/damonholland777/Desktop/trading_bot/strategy_consensus.py

# Auto-Execution
/usr/bin/python3 /Users/damonholland777/Desktop/trading_bot/auto_execute_consensus_trades.py

echo "✅ All tasks completed."
