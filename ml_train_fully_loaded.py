import logging
import time
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, RandomizedSearchCV, train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import ta

logging.basicConfig(level=logging.INFO)

def load_data(filepath):
    logging.info(f"Loading data from {filepath}")
    df = pd.read_json(filepath)
    
    # Convert timestamps if present
    if 'open_time' in df.columns:
        df['timestamp'] = pd.to_datetime(df['open_time'])
    
    # Use close price as main price feature
    if 'close' in df.columns:
        df['price'] = df['close'].astype(float)
    elif 'price' in df.columns:
        df['price'] = df['price'].astype(float)
    else:
        raise ValueError("No price column found in data")

    return df

def add_technical_indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['price']).rsi().bfill()
    df['atr'] = ta.volatility.AverageTrueRange(high=df['high'], low=df['low'], close=df['close']).average_true_range().bfill()
    bb_indicator = ta.volatility.BollingerBands(close=df['close'])
    df['bb_width'] = (bb_indicator.bollinger_hband() - bb_indicator.bollinger_lband()).bfill()
    df['volume'] = df['volume'].astype(float)
    
    # Moving averages
    df['ma_5'] = df['price'].rolling(window=5).mean().bfill()
    df['ma_10'] = df['price'].rolling(window=10).mean().bfill()
    df['ma_20'] = df['price'].rolling(window=20).mean().bfill()

    return df

def create_features(df, window=5):
    X, y = [], []
    for i in range(window, len(df) - 1):
        features = []
        for j in range(i - window, i):
            features.extend([
                df.iloc[j]['price'],
                df.iloc[j]['rsi'],
                df.iloc[j]['atr'],
                df.iloc[j]['bb_width'],
                df.iloc[j]['volume'],
                df.iloc[j]['ma_5'],
                df.iloc[j]['ma_10'],
                df.iloc[j]['ma_20'],
            ])
        X.append(features)
        y.append(df.iloc[i + 1]['price'])
    return np.array(X), np.array(y)

def train_and_tune(data_file='binance_btc_3yrs_chunked.json'):
    df = load_data(data_file)
    df = add_technical_indicators(df)

    X, y = create_features(df)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    param_dist = {
        'n_estimators': [100, 200, 300, 400],
        'max_depth': [10, 20, 30, 40, None],
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
    joblib.dump(scaler, 'scaler.joblib')

    print(f"Best hyperparameters: {rand_search.best_params_}")
    print(f"Mean Squared Error on test set: {mse:.4f}")

def autotune_loop(interval_minutes=60, data_file='binance_btc_3yrs_chunked.json'):
    while True:
        print(f"Starting training cycle at {datetime.now()}...")
        train_and_tune(data_file)
        print(f"Sleeping for {interval_minutes} minutes...")
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    # Run a single training pass now:
    train_and_tune()

    # To enable auto-tuning every hour, uncomment below:
    # autotune_loop(interval_minutes=60)
