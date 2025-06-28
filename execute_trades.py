#!/usr/bin/env python3
import os
import ccxt
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv(os.path.expanduser("~/Desktop/trading_bot/.env"))

api_key = os.getenv("BINANCE_US_API_KEY")
secret_key = os.getenv("BINANCE_US_SECRET_KEY")

# Initialize Binance.US
exchange = ccxt.binanceus({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
})

# Config: which symbols to trade and per-trade USD amount
TRADE_SYMBOLS = ["ADA/USDT", "SOL/USDT", "BNB/USDT"]
TRADE_AMOUNT_USD = 1.0

# Load trade signals CSV
signals_path = "./data/lstm_trade_signals.csv"
df = pd.read_csv(signals_path)

# Get the latest row of signals
latest_signals = df.iloc[-1]
timestamp = latest_signals["timestamp"]

# Prepare log entries
log_entries = []

for col in latest_signals.index:
    if col == "timestamp":
        continue

    signal = latest_signals[col]
    base_symbol = col.replace("_target_return", "")
    symbol = f"{base_symbol}/USDT"

    if symbol not in TRADE_SYMBOLS:
        print(f"⚠️ Skipping {symbol} due to min notional restriction.")
        continue

    if signal == "HOLD":
        print(f"ℹ️ {symbol}: HOLD signal. No action taken.")
        continue

    try:
        # Fetch current price
        ticker = exchange.fetch_ticker(symbol)
        price = ticker["last"]

        # Calculate amount to buy/sell
        amount = TRADE_AMOUNT_USD / price

        # Create order
        side = "buy" if signal == "BUY" else "sell"
        order = exchange.create_market_order(symbol, side, amount)

        print(f"✅ {symbol}: Executed {side.upper()} {amount:.4f} at {price:.4f}")

        log_entries.append({
            "timestamp": timestamp,
            "symbol": symbol,
            "side": side,
            "price": price,
            "amount": amount,
            "status": "executed"
        })

    except Exception as e:
        print(f"❌ {symbol}: Error executing order: {e}")
        log_entries.append({
            "timestamp": timestamp,
            "symbol": symbol,
            "side": signal.lower(),
            "price": None,
            "amount": None,
            "status": f"error: {e}"
        })

# Save log to CSV
log_df = pd.DataFrame(log_entries)
log_file = "./data/trade_execution_log.csv"
log_df.to_csv(log_file, index=False)
print(f"🎯 Trade execution log saved to {log_file}")
