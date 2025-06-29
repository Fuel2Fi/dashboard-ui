#!/usr/bin/env python3
import os
import json
import ccxt
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

# Load strategy output
strategy_output = None
try:
    output = os.popen("python3 ~/Desktop/trading_bot/strategy_engine.py").read()
    strategy_output = json.loads(output)
except Exception as e:
    print(f"❌ Error loading strategy output: {e}")
    exit(1)

print("🚀 Auto Executor Running...")

log_lines = []

for action in strategy_output["actions"]:
    symbol = action["symbol"]
    signal = action["signal"]
    action_type = action["action"]

    if action_type == "hold":
        print(f"✅ {symbol}: No action (hold)")
        continue

    try:
        # Fetch ticker to estimate quantity
        ticker = exchange.fetch_ticker(symbol.replace("USDT", "/USDT"))
        last_price = ticker["last"]
        qty = round(10.0 / last_price, 6)

        # Determine side
        side = "buy" if action_type == "open_long" else "sell"

        # Place order
        order = exchange.create_market_order(
            symbol=symbol.replace("USDT", "/USDT"),
            side=side,
            amount=qty
        )
        msg = f"{side.upper()} order placed: {qty} {symbol}"
        print(f"✅ {symbol}: {msg}")

        log_lines.append(f"{strategy_output['timestamp']},{symbol},{signal},{msg},{datetime.utcnow().isoformat()}")
    except Exception as e:
        err = f"ERROR: {e}"
        print(f"✅ {symbol}: {err}")
        log_lines.append(f"{strategy_output['timestamp']},{symbol},{signal},{err},{datetime.utcnow().isoformat()}")

# Write log
log_file = "./data/live_trade_log.csv"
header = "timestamp,symbol,signal,result,executed_at\n"
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write(header)

with open(log_file, "a") as f:
    for line in log_lines:
        f.write(line + "\n")

print("✅ All signals processed.")
