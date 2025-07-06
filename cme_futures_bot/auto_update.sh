#!/bin/bash

# Activate your Python environment
source ~/Desktop/trading_bot/env/bin/activate
cd ~/Desktop/trading_bot/cme_futures_bot

echo "🚀 Running full auto-update at \$(date)"

# Re-run all backtests
python backtest_selector.py

# Generate performance summaries
python generate_strategy_performance.py

# Run auto-tuner
python auto_tuner.py

# Run strategy engine
python strategy_engine.py

echo "✅ Auto-update complete at \$(date)"
