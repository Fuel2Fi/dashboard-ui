#!/usr/bin/env python3
import os
import time
import hmac
import hashlib
import requests

API_KEY = os.environ.get("BITUNIX_API_KEY")
API_SECRET = os.environ.get("BITUNIX_API_SECRET").encode()

BASE_URL = "https://api.bitunix.com"

def sign_payload(payload):
    sorted_items = sorted(payload.items())
    query_string = "&".join([f"{k}={v}" for k, v in sorted_items])
    signature = hmac.new(API_SECRET, query_string.encode(), hashlib.sha256).hexdigest()
    return signature

def get_server_time():
    return int(time.time() * 1000)

def get_price(symbol):
    url = f"{BASE_URL}/api/v1/market/ticker"
    r = requests.get(url, params={"symbol": symbol})
    r.raise_for_status()
    return float(r.json()["data"]["lastPrice"])

def get_balance():
    """
    Fetch Futures account balance.
    """
    url = f"{BASE_URL}/api/v1/private/position/account"
    ts = get_server_time()
    payload = {"timestamp": ts}
    signature = sign_payload(payload)
    payload["signature"] = signature
    headers = {"X-BX-APIKEY": API_KEY}
    r = requests.get(url, headers=headers, params=payload)
    r.raise_for_status()
    return r.json()

def place_order(symbol, side, max_usd=10):
    """
    Place a market order in the Futures market.
    """
    price = get_price(symbol)
    quantity = round(max_usd / price, 4)

    # Enforce minimum quantity
    if "BTC" in symbol and quantity < 0.001:
        quantity = 0.001
    if "ETH" in symbol and quantity < 0.01:
        quantity = 0.01

    url = f"{BASE_URL}/api/v1/private/order/submit"
    ts = get_server_time()
    payload = {
        "symbol": symbol,
        "side": side.upper(),  # BUY or SELL
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": ts
    }
    signature = sign_payload(payload)
    payload["signature"] = signature
    headers = {"X-BX-APIKEY": API_KEY}
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code != 200:
        raise Exception(f"Order failed: {r.text}")
    return r.json()
