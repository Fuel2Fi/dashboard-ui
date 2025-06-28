import json
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def compute_rsi(prices, window=14):
    deltas = np.diff(prices)
    seed = deltas[:window]
    up = seed[seed >= 0].sum()/window
    down = -seed[seed < 0].sum()/window
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:window] = 100. - 100./(1.+rs)

    for i in range(window, len(prices)):
        delta = deltas[i-1]
        upval = max(delta, 0)
        downval = -min(delta, 0)
        up = (up*(window-1) + upval)/window
        down = (down*(window-1) + downval)/window
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100./(1.+rs)
    return rsi

def compute_macd(prices, slow=26, fast=12, signal=9):
    exp1 = np.zeros_like(prices)
    exp2 = np.zeros_like(prices)
    ema_fast = prices[0]
    ema_slow = prices[0]
    alpha_fast = 2/(fast+1)
    alpha_slow = 2/(slow+1)
    for i in range(len(prices)):
        ema_fast = alpha_fast*prices[i] + (1 - alpha_fast)*ema_fast
        ema_slow = alpha_slow*prices[i] + (1 - alpha_slow)*ema_slow
        exp1[i] = ema_fast
        exp2[i] = ema_slow
    macd_line = exp1 - exp2
    signal_line = np.zeros_like(prices)
    ema_signal = macd_line[0]
    alpha_signal = 2/(signal+1)
    for i in range(len(macd_line)):
        ema_signal = alpha_signal*macd_line[i] + (1-alpha_signal)*ema_signal
        signal_line[i] = ema_signal
    macd_hist = macd_line - signal_line
    return macd_line, signal_line, macd_hist

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    prices = np.array([entry['price'] for entry in data])
    return prices

def create_features(prices, window_size=5):
    rsi = compute_rsi(prices)
    macd_line, signal_line, macd_hist = compute_macd(prices)
    X, y = [], []
    for i in range(window_size, len(prices)-1):
        features = []
        # price window
        features.extend(prices[i-window_size:i])
        # RSI value at i
        features.append(rsi[i])
        # MACD histogram at i
        features.append(macd_hist[i])
        X.append(features)
        y.append(prices[i+1])
    return np.array(X), np.array(y)

def main():
    prices = load_data('mock_price_data.json')
    X, y = create_features(prices)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)

    print(f"Mean Squared Error on test set: {mse:.4f}")

    example_input = X_test[0].reshape(1, -1)
    prediction = model.predict(example_input)[0]
    print(f"Predicted next price: {prediction:.2f}")
    print(f"Actual next price: {y_test[0]:.2f}")

if __name__ == "__main__":
    main()
