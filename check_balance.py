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

def get_account_balance():
    timestamp = get_server_time()
    params = {"timestamp": timestamp}
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(API_SECRET, query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": API_KEY}
    url = f"{BASE_URL}/api/v3/account"
    r = requests.get(url, headers=headers, params=params)
    return r.json()

balances = get_account_balance()
for asset in balances["balances"]:
    if float(asset["free"]) > 0:
        print(f"{asset['asset']}: {asset['free']}")
