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

# Initialize Binance.US
exchange = ccxt.binanceus({
    "apiKey": api_key,
    "secret": secret_key,
    "enableRateLimit": True,
})

# Load consensus decisions
with open("./strategy_consensus_output.json", "r") as f:
    consensus = json.load(f)

# Fixed trade amount
USDT_AMOUNT = 10.0

# Open log file
log_file = "./data/consensus_live_trade_log.csv"
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write("timestamp,symbol,signal,result,executed_at\n")

print("🚀 Auto-Executor from Consensus Starting...")

for decision in consensus["decisions"]:
    symbol = decision["symbol"].replace("USDT", "/USDT")
    signal = decision["consensus_signal"]
    ts = consensus["timestamp"]

    if signal == "hold":
        print(f"✅ {symbol}: No action (HOLD).")
        with open(log_file, "a") as f:
            f.write(f"{ts},{symbol},{signal},HOLD,{datetime.utcnow().isoformat()}\n")
        continue

    side = "buy" if signal == "buy" else "sell"

    try:
        # Get market price to compute quantity
        ticker = exchange.fetch_ticker(symbol)
        last_price = ticker["last"]
        qty = round(USDT_AMOUNT / last_price, 6)

        # Place order
        order = exchange.create_market_order(symbol, side, qty)
        result_msg = f"{side.upper()} order placed: {qty} {symbol.split('/')[0]}"

        print(f"✅ {symbol}: {result_msg}")
        with open(log_file, "a") as f:
            f.write(f"{ts},{symbol},{signal},{result_msg},{datetime.utcnow().isoformat()}\n")

    except Exception as e:
        error_msg = f"ERROR: {e}"
        print(f"❌ {symbol}: {error_msg}")
        with open(log_file, "a") as f:
            f.write(f"{ts},{symbol},{signal},{error_msg},{datetime.utcnow().isoformat()}\n")
