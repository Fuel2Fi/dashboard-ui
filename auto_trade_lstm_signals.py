#!/usr/bin/env python3
import os
import csv
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

def place_order(symbol, side, usdt_amount):
    try:
        ticker = exchange.fetch_ticker(symbol)
        last_price = ticker["last"]
        qty = round(usdt_amount / last_price, 6)
        order = exchange.create_market_order(
            symbol=symbol,
            side=side,
            amount=qty
        )
        return f"{side.upper()} order placed: {qty} {symbol.split('/')[0]} for ~{usdt_amount} USDT"
    except Exception as e:
        return f"ERROR: {e}"

def main():
    print("🚀 Automated Trade Executor Starting...")
    signals_file = "./data/lstm_trade_signals.csv"
    log_file = "./data/live_trade_log.csv"

    if not os.path.exists(signals_file):
        print("❌ Signals file not found.")
        return

    with open(signals_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("❌ No signals to execute.")
        return

    latest = rows[0]
    timestamp = latest["timestamp"]
    print(f"✅ Executing signals for {timestamp}")

    results = []

    for pair_col in ["BTCUSDT_target_return", "ETHUSDT_target_return", "ADAUSDT_target_return", "SOLUSDT_target_return", "BNBUSDT_target_return"]:
        signal = latest[pair_col].strip().upper()
        if signal == "HOLD":
            continue

        base_symbol = pair_col.split("_")[0].replace("USDT", "")
        symbol = f"{base_symbol}/USDT"

        result = place_order(symbol, signal.lower(), 10.0)
        results.append({
            "timestamp": timestamp,
            "symbol": symbol,
            "signal": signal,
            "result": result,
            "executed_at": datetime.utcnow().isoformat()
        })

    # Append log
    log_exists = os.path.exists(log_file)
    with open(log_file, "a", newline="") as f:
        fieldnames = ["timestamp", "symbol", "signal", "result", "executed_at"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not log_exists:
            writer.writeheader()
        for r in results:
            writer.writerow(r)

    print(f"✅ {len(results)} trades executed and logged.")

if __name__ == "__main__":
    main()
