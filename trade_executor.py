#!/usr/bin/env python3
import ccxt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Initialize exchange
exchange = ccxt.binance({
    "apiKey": BINANCE_API_KEY,
    "secret": BINANCE_SECRET_KEY,
    "enableRateLimit": True,
})

# Fetch account balance
balance = exchange.fetch_balance()
print("✅ Account balances:")
for currency, details in balance['total'].items():
    if details > 0:
        print(f"{currency}: {details}")

# Fetch ticker data for BTC/USDT
ticker = exchange.fetch_ticker('BTC/USDT')
print("\n✅ BTC/USDT Ticker:")
print(f"Last Price: {ticker['last']}")
print(f"Bid: {ticker['bid']}")
print(f"Ask: {ticker['ask']}")
