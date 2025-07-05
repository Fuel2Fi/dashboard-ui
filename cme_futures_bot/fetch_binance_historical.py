import json
import pandas as pd
from binance.client import Client

# Load API keys
with open("secrets.json") as f:
    keys = json.load(f)

api_key = keys["binance_api_key"]
api_secret = keys["binance_api_secret"]

# Initialize Binance.US client
client = Client(api_key, api_secret, tld="us")

# Fetch historical daily data for BTCUSDT
klines = client.get_historical_klines(
    "BTCUSDT",
    Client.KLINE_INTERVAL_1DAY,
    "1 Jan, 2017"
)

# Convert to DataFrame
columns = [
    "OpenTime", "Open", "High", "Low", "Close", "Volume",
    "CloseTime", "QuoteAssetVolume", "NumberOfTrades",
    "TakerBuyBaseVolume", "TakerBuyQuoteVolume", "Ignore"
]
df = pd.DataFrame(klines, columns=columns)

# Keep relevant columns and format
df = df[["OpenTime", "Open", "High", "Low", "Close", "Volume"]]
df["Date"] = pd.to_datetime(df["OpenTime"], unit='ms')
df.set_index("Date", inplace=True)
df = df.drop(columns=["OpenTime"])
df = df.astype(float)

# Save to CSV
df.to_csv("historical_data.csv")
print("\\n✅ BTCUSDT historical data saved to 'historical_data.csv'")
