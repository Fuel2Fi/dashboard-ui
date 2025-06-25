import requests
import time
from data_sources.coingecko.token_config import TOKEN_LIST

def test_token(token):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": token,
        "vs_currencies": "usd"
    }

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if token in data:
            price = data[token]["usd"]
            print(f"✅ {token:<20} | ${price}")
        else:
            print(f"❌ {token:<20} | No data returned")
    except Exception as e:
        print(f"❌ {token:<20} | ERROR: {e}")

def fetch_prices(token_list):
    API_KEY = "CG-Dmr9nrkm5dDzT3rW6NVVMv1v"
    HEADERS = {"x-cg-pro-api-key": API_KEY}

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(token_list),
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("⚠️ Error fetching batch data from CoinGecko:", e)
        return None

# 🧪 THIS FUNCTION NOW PRINTS RAW RESPONSE FOR DEBUGGING
def fetch_price_from_coingecko(token):
    API_KEY = "CG-Dmr9nrkm5dDzT3rW6NVVMv1v"
    HEADERS = {"x-cg-pro-api-key": API_KEY}

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": token,
        "vs_currencies": "usd"
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"[DEBUG] Raw response for '{token}': {data}")
        return data.get(token, {}).get("usd", None)
    except Exception as e:
        print(f"❌ [fetch_price_from_coingecko] Error fetching {token}: {e}")
        return None

if __name__ == "__main__":
    print("🔍 Testing all tokens one-by-one...\n")
    for token in TOKEN_LIST:
        test_token(token)
        time.sleep(1.5)
