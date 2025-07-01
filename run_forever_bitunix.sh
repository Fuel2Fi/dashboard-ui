#!/bin/bash
while true; do
  echo "🔄 Running Bitunix Futures Bot at $(date)"
  python /Users/damonholland777/Desktop/trading_bot/manage_positions.py
  echo "✅ Cycle complete. Sleeping 300 seconds..."
  sleep 300
done
