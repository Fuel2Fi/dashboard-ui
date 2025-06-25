import json
import matplotlib.pyplot as plt

# Load the merged data from JSON
with open("merged_data.json", "r") as f:
    data = json.load(f)

tokens = []
binance_prices = []
coingecko_prices = []
averages = []

for token, values in data.items():
    tokens.append(token.title())
    binance_prices.append(values['binance'])
    coingecko_prices.append(values['coingecko'])
    averages.append(values['average_price'])

x = range(len(tokens))

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(x, binance_prices, width=0.25, label='Binance.US', align='center')
plt.bar([i + 0.25 for i in x], coingecko_prices, width=0.25, label='CoinGecko', align='center')
plt.plot([i + 0.125 for i in x], averages, color='black', marker='o', label='Avg Price')

plt.xticks([i + 0.125 for i in x], tokens, rotation=45)
plt.ylabel('Price (USD)')
plt.title('🧠 Merged Token Feed: Binance.US vs CoinGecko')
plt.legend()
plt.tight_layout()
plt.grid(True)

plt.show()
