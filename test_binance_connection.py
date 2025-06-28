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

try:
    balance = exchange.fetch_balance()
    print("✅ Connection successful. Balances:")
    for asset, info in balance['total'].items():
        if info > 0:
            print(f"{asset}: {info}")
except Exception as e:
    print(f"❌ Error connecting to Binance.US: {e}")
