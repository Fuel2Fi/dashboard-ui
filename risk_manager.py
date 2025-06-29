#!/usr/bin/env python3
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import ccxt

# Load environment variables
load_dotenv(os.path.expanduser("~/Desktop/trading_bot/.env"))
api_key = os.getenv("BINANCE_US_API_KEY")
secret_key = os.getenv("BINANCE_US_SECRET_KEY")

exchange = ccxt.binanceus({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
})

POSITIONS_FILE = os.path.expanduser("~/Desktop/trading_bot/data/positions.json")
STOP_LOSS_PERCENT = 0.02  # 2%
TAKE_PROFIT_PERCENT = 0.03  # 3%
TRAILING_BUFFER = 0.005  # 0.5%

def load_positions():
    if not os.path.exists(POSITIONS_FILE):
        return {}
    with open(POSITIONS_FILE, "r") as f:
        return json.load(f)

def save_positions(positions):
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=2)

def fetch_balance_for_asset(symbol):
    """Fetches the free balance of a given asset symbol."""
    balance = exchange.fetch_balance()
    return balance.get(symbol, {}).get("free", 0)

def monitor_positions(positions):
    updated_positions = positions.copy()
    for symbol, data in positions.items():
        side = data["side"]
        qty = float(data["qty"])
        avg_price = float(data["average_price"])

        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker["last"]

        if side == "buy":
            stop_loss_price = avg_price * (1 - STOP_LOSS_PERCENT)
            take_profit_price = avg_price * (1 + TAKE_PROFIT_PERCENT + TRAILING_BUFFER)
            if current_price <= stop_loss_price:
                close_side = "sell"
                reason = "Stop loss hit"
            elif current_price >= take_profit_price:
                close_side = "sell"
                reason = "Take profit hit"
            else:
                continue
        elif side == "sell":
            stop_loss_price = avg_price * (1 + STOP_LOSS_PERCENT)
            take_profit_price = avg_price * (1 - TAKE_PROFIT_PERCENT - TRAILING_BUFFER)
            if current_price >= stop_loss_price:
                close_side = "buy"
                reason = "Stop loss hit"
            elif current_price <= take_profit_price:
                close_side = "buy"
                reason = "Take profit hit"
            else:
                continue
        else:
            continue

        # Verify balance before closing
        base_asset = symbol.split("/")[0]
        available_qty = fetch_balance_for_asset(base_asset)
        if available_qty < qty * 0.99:  # Allow minor rounding
            print(f"⚠️ Skipping close of {symbol}: Insufficient balance (needed {qty}, available {available_qty})")
            continue

        # Execute close order
        try:
            order = exchange.create_market_order(symbol, close_side, qty)
            print(f"✅ {reason}: {close_side.upper()} order placed for {qty} {symbol}.")
            del updated_positions[symbol]
        except Exception as e:
            print(f"❌ Error closing {symbol}: {e}")
    return updated_positions

def main():
    print("🔍 Monitoring positions with balance verification...")
    positions = load_positions()
    if not positions:
        print("✅ No open positions to monitor.")
        return
    positions = monitor_positions(positions)
    save_positions(positions)
    print("✅ Monitoring complete.")

if __name__ == "__main__":
    main()
