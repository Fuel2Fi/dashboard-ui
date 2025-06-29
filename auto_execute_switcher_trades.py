#!/usr/bin/env python3
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import ccxt

# Load .env
load_dotenv(os.path.expanduser("~/Desktop/trading_bot/.env"))

api_key = os.getenv("BINANCE_US_API_KEY")
secret_key = os.getenv("BINANCE_US_SECRET_KEY")

# Initialize exchange
exchange = ccxt.binanceus({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
})

# Load switcher output
with open("./strategy_switcher_output.json", "r") as f:
    switcher_data = json.load(f)

print("🚀 Auto-Executor from Strategy Switcher Starting...")

# For each decision
for d in switcher_data["decisions"]:
    symbol = d["symbol"]
    decision = d["decision"]
    usdt_amount = 10  # Adjust trade size as desired

    if decision == "hold":
        print(f"✅ {symbol}: No action (HOLD).")
        continue

    base = symbol.replace("USDT","")
    pair = f"{base}/USDT"
    side = "buy" if decision == "buy" else "sell"

    # Estimate quantity
    try:
        ticker = exchange.fetch_ticker(pair)
        price = ticker["last"]
        qty = round(usdt_amount / price,6)
    except Exception as e:
        print(f"❌ {symbol}: Error fetching ticker: {e}")
        continue

    # Place order
    try:
        order = exchange.create_market_order(pair, side, qty)
        print(f"✅ {symbol}: {side.upper()} order placed ({qty})")
    except Exception as e:
        print(f"❌ {symbol}: Error placing order: {e}")

