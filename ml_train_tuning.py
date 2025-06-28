import json
import logging
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV, KFold, train_test_split
from sklearn.metrics import mean_squared_error
import ta  # technical analysis library

logging.basicConfig(level=logging.INFO)

DATA_FILE = 'binance_live_data.json'  # Or mock_price_data.json for testing

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['price'] = df['price'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def add_technical_indicators(df):
    # Momentum indicators
    df['rsi'] = ta.momentum.RSIIndicator(df['price']).rsi()
    df['stoch_k'] = ta.momentum.StochasticOscillator(df['price'], df['price'], df['price']).stoch()
    df['stoch_d'] = ta.momentum.StochasticOscillator(df['price'], df['price'], df['price']).stoch_signal()

    # Trend indicators
    macd = ta.trend.MACD(df['price'])
    df['macd_hist'] = macd.macd_diff()
    df['adx'] = ta.trend.ADXIndicator(df['price'], df['price'], df['price']).adx()

    # Volatility indicators
    df['atr'] = ta.volatility.AverageTrueRange(df['price'], df['price'], df['price']).average_true_range()
    bollinger = ta.volatility.BollingerBands(df['price'])
    df['bollinger_h'] = bollinger.bollinger_hband()
    df['bollinger_l'] = bollinger.bollinger_lband()

    # Fill missing values forward then backward
    df.ffill(inplace=True)
    df.bfill(inplace=True)

    return df

def create_features(df, window=10):
    X, y = [], []
    for i in range(window, len(df) - 1):
        features = []
        for j in range(window):
            features.extend([
                df.iloc[i - window + j]['price'],
                df.iloc[i - window + j]['rsi'],
                df.iloc[i - window + j]['stoch_k'],
                df.iloc[i - window + j]['stoch_d'],
                df.iloc[i - window + j]['macd_hist'],
                df.iloc[i - window + j]['adx'],
                df.iloc[i - window + j]['atr'],
                df.iloc[i - window + j]['bollinger_h'],
                df.iloc[i - window + j]['bollinger_l'],
            ])
        X.append(features)
        y.append(df.iloc[i + 1]['price'])
    return np.array(X), np.array(y)

def train_and_tune():
    logging.info(f"Loading data from {DATA_FILE}")
    df = load_data(DATA_FILE)
    df = add_technical_indicators(df)
    X, y = create_features(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_dist = {
        'n_estimators': [50, 100, 200, 300],
        'max_depth': [5, 10, 20, 40, None],
        'min_samples_split': [2, 5, 10, 15],
        'min_samples_leaf': [1, 2, 4, 6]
    }

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    model = RandomForestRegressor(random_state=42)
    rand_search = RandomizedSearchCV(
        model,
        param_distributions=param_dist,
        n_iter=30,  # More iterations for better tuning
        cv=cv,
        scoring='neg_mean_squared_error',
        random_state=42,
        n_jobs=-1
    )
    rand_search.fit(X_train, y_train)

    best_model = rand_search.best_estimator_
    preds = best_model.predict(X_test)
    mse = mean_squared_error(y_test, preds)

    logging.info(f"Training done. Best params: {rand_search.best_params_}, MSE: {mse:.4f}")

    print(f"Best hyperparameters: {rand_search.best_params_}")
    print(f"Mean Squared Error on test set: {mse:.4f}")

if __name__ == "__main__":
    train_and_tune()
