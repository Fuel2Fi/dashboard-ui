#!/usr/bin/env python3
import os
import csv
import time
from datetime import datetime
from dotenv import load_dotenv
import ccxt

# Load environment variables
load_dotenv(os.path.expanduser("~/Desktop/trading_bot/.env"))

api_key = os.getenv("BINANCE_US_API_KEY")
secret_key = os.getenv("BINANCE_US_SECRET_KEY")

# Initialize Binance.US client
exchange = ccxt.binanceus({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
})

# Parameters
TRADE_AMOUNT_USD = 10  # Amount to trade per order
SIGNAL_FILE = "./data/lstm_trade_signals.csv"
LOG_FILE = "./data/executed_trades.csv"

# Load signals
signals = []
with open(SIGNAL_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        signals.append(row)

# Process signals
for row in signals:
    timestamp = row["timestamp"]
    print(f"\n=== {timestamp} ===")
    for symbol_col, signal in row.items():
        if symbol_col == "timestamp":
            continue

        base_symbol = symbol_col.replace("_target_return", "")
        market_symbol = base_symbol.replace("USDT", "/USDT")

        if signal == "HOLD":
            print(f"{base_symbol}: HOLD - no action.")
            continue

        try:
            # Fetch current price
            ticker = exchange.fetch_ticker(market_symbol)
            last_price = ticker["last"]
            qty = round(TRADE_AMOUNT_USD / last_price, 6)

            # Determine side
            side = "buy" if signal == "BUY" else "sell"

            print(f"{base_symbol}: {signal} - Placing market {side.upper()} order for ~${TRADE_AMOUNT_USD}")

            # Place market order
            order = exchange.create_market_order(
                symbol=market_symbol,
                side=side,
                amount=qty
            )

            # Log trade
            log_row = [
                datetime.utcnow().isoformat(),
                base_symbol,
                signal,
                side,
                qty,
                order['id'],
                order['status'],
                last_price
            ]
            with open(LOG_FILE, "a", newline="") as logfile:
                writer = csv.writer(logfile)
                writer.writerow(log_row)

            print(f"✅ Order placed. ID: {order['id']} Status: {order['status']}")

            time.sleep(1)  # Sleep to respect rate limits

        except Exception as e:
            print(f"❌ Error placing order for {base_symbol}: {e}")

print("\n🎯 All signals processed.")
