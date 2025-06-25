from flask import Flask, send_file
import matplotlib.pyplot as plt
import json
import io

app = Flask(__name__)

@app.route("/")
def chart():
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

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, binance_prices, width=0.25, label='Binance.US', align='center')
    ax.bar([i + 0.25 for i in x], coingecko_prices, width=0.25, label='CoinGecko', align='center')
    ax.plot([i + 0.125 for i in x], averages, color='black', marker='o', label='Avg Price')
    ax.set_xticks([i + 0.125 for i in x])
    ax.set_xticklabels(tokens, rotation=45)
    ax.set_ylabel('Price (USD)')
    ax.set_title('Merged Token Feed: Binance.US vs CoinGecko')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')
