from binance.spot import Spot
from config import API_KEY, API_SECRET

# Authenticated client for Binance.US
client = Spot(api_key=API_KEY, api_secret=API_SECRET, base_url="https://api.binance.us")
