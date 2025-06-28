import json
import time
import logging
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV, KFold, train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import ta  # Technical analysis library
import requests

logging.basicConfig(level=logging.INFO)

BINANCE_SYMBOL = 'BTCUSDT'
BINANCE_INTERVAL = '1d'
BINANCE_API_URL = 'https://api.binance.us/api/v3/klines'
DATA_FILE = 'binance_live_data.json'

def fetch_live_binance_data(symbol=BINANCE_SYMBOL, interval=BINANCE_INTERVAL, limit=1000):
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    logging.info(f"Fetching live data from Binance: {symbol}, interval: {interval}, limit: {limit}")
    response = requests.get(BINANCE_API_URL, params=params)
    response.raise_for_status()
    raw_data = response.json()

    formatted_data = []
    for entry in raw_data:
        formatted_data.append({
            'timestamp': datetime.utcfromtimestamp(entry[0] / 1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'price': float(entry[4])  # Closing price
        })
    with open(DATA_FILE, 'w') as f:
        json.dump(formatted_data, f, indent=2)
    logging.info(f"Saved {len(formatted_data)} data points to {DATA_FILE}")

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['price'] = df['price'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def add_technical_indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['price']).rsi()
    macd = ta.trend.MACD(df['price'])
    df['macd_hist'] = macd.macd_diff()
    df['atr'] = ta.volatility.AverageTrueRange(high=df['price'], low=df['price'], close=df['price']).average_true_range()
    df['bollinger_h'] = ta.volatility.BollingerBands(df['price']).bollinger_hband()
    df['bollinger_l'] = ta.volatility.BollingerBands(df['price']).bollinger_lband()

    df.bfill(inplace=True)
    return df

def create_features(df, window=5):
    X, y = [], []
    for i in range(window, len(df) - 1):
        features = []
        for j in range(window):
            features.extend([
                df.iloc[i - window + j]['price'],
                df.iloc[i - window + j]['rsi'],
                df.iloc[i - window + j]['macd_hist'],
                df.iloc[i - window + j]['atr'],
                df.iloc[i - window + j]['bollinger_h'],
                df.iloc[i - window + j]['bollinger_l'],
            ])
        X.append(features)
        y.append(df.iloc[i + 1]['price'])
    return np.array(X), np.array(y)

def train_and_tune():
    fetch_live_binance_data()  # Fetch fresh data before training

    logging.info(f"Loading data from {DATA_FILE}")
    df = load_data(DATA_FILE)
    df = add_technical_indicators(df)
    X, y = create_features(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_dist = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    model = RandomForestRegressor(random_state=42)
    rand_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=15,
                                     cv=cv, scoring='neg_mean_squared_error',
                                     random_state=42, n_jobs=-1)
    rand_search.fit(X_train, y_train)

    best_model = rand_search.best_estimator_
    preds = best_model.predict(X_test)
    mse = mean_squared_error(y_test, preds)

    logging.info(f"Training done. Best params: {rand_search.best_params_}, MSE: {mse:.4f}")

    joblib.dump(best_model, 'trained_model.joblib')

    print(f"Best hyperparameters: {rand_search.best_params_}")
    print(f"Mean Squared Error on test set: {mse:.4f}")

def autotune_loop(interval_minutes=60):
    while True:
        print(f"Starting training cycle at {datetime.now()}...")
        train_and_tune()
        print(f"Sleeping for {interval_minutes} minutes...")
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    autotune_loop(interval_minutes=60)
