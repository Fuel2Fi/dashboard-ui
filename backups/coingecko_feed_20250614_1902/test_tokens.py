# test_tokens.py

import requests
from data_sources.coingecko.token_config import TOKEN_LIST

API_KEY = "PUT-YOUR-API-KEY-HERE"  # Replace with your API key
HEADERS = {"x-cg-pro-api-key": API_KEY}

def test_token(token):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": token,
        "vs_currencies": "usd"
    }

    try:
        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        data = r.json()
        if token in data:
            return True
        else:
            return False
    except:
        return False

if __name__ == "__main__":
    print("🔍 Testing token list...\n")
    for token in TOKEN_LIST:
        is_valid = test_token(token)
        status = "✅ VALID" if is_valid else "❌ INVALID"
        print(f"{token:<20} {status}")

