#!/usr/bin/env python3
import os
import time
import hmac
import hashlib
import requests

API_KEY = os.environ.get("BINANCE_API_KEY")
API_SECRET = os.environ.get("BINANCE_API_SECRET").encode()

BASE_URL = "https://api.binance.us"

def get_server_time():
    url = f"{BASE_URL}/api/v3/time"
    r = requests.get(url)
    return r.json()["serverTime"]

def get_price(symbol):
    url = f"{BASE_URL}/api/v3/ticker/price"
    r = requests.get(url, params={"symbol": symbol})
    return float(r.json()["price"])

def place_order(symbol, side, max_usd=10):
    price = get_price(symbol)
    quantity = round(max_usd / price, 6)

    # Apply Binance.US min quantity per symbol
    if "BTC" in symbol and quantity < 0.0001:
        quantity = 0.0001
    if "ETH" in symbol and quantity < 0.001:
        quantity = 0.001
    if "SOL" in symbol and quantity < 0.01:
        quantity = 0.01
    if "ADA" in symbol and quantity < 1:
        quantity = 1

    # Round quantity to 6 decimals to comply with step size
    quantity = round(quantity, 6)

    timestamp = get_server_time()
    params = {
        "symbol": symbol,
        "side": side.upper(),
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": timestamp,
    }

    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(API_SECRET, query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature

    headers = {
        "X-MBX-APIKEY": API_KEY
    }

    url = f"{BASE_URL}/api/v3/order"
    response = requests.post(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Order failed: {response.text}")

    return response.json()
