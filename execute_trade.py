#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import ccxt

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

def place_order(symbol, side, usdt_amount):
    """Place a market order on Binance.US"""
    try:
        # Fetch current ticker to estimate price
        ticker = exchange.fetch_ticker(symbol)
        last_price = ticker["last"]
        qty = round(usdt_amount / last_price, 6)

        # Place order
        order = exchange.create_market_order(
            symbol=symbol,
            side=side,
            amount=qty
        )
        print(f"✅ {side.upper()} order placed: {qty} {symbol.split('/')[0]} for ~{usdt_amount} USDT.")
    except Exception as e:
        print(f"❌ Error placing order: {e}")

if __name__ == "__main__":
    print("Binance.US Live Trade Executor (Testing Mode)")
    print("---------------------------------------------")
    symbol = input("Enter trading pair (e.g., BTC/USDT): ").strip().upper()
    side = input("Enter side (buy or sell): ").strip().lower()
    usdt_amount = 1.0  # Hard-coded to $1 per trade
    print(f"Using fixed trade size: {usdt_amount} USDT.")
    confirm = input(f"CONFIRM: Place {side.upper()} order for approx {usdt_amount} USDT of {symbol}? (yes/no): ").strip().lower()
    if confirm == "yes":
        place_order(symbol, side, usdt_amount)
    else:
        print("❌ Cancelled.")
