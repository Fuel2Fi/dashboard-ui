import json
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import joblib
import logging
import ta  # Technical analysis library

logging.basicConfig(level=logging.INFO)

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    # Adjust for Binance OHLCV format fields
    if 'close' in df.columns:
        df['close'] = df['close'].astype(float)
        df['price'] = df['close']  # Alias close as price for compatibility
    else:
        raise KeyError("Expected 'close' field not found in data.")
    if 'volume' in df.columns:
        df['volume'] = df['volume'].astype(float)
    else:
        df['volume'] = 0.0
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    elif 'open_time' in df.columns:
        df['timestamp'] = pd.to_datetime(df['open_time'])
    else:
        df['timestamp'] = pd.to_datetime('now')
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df

def add_technical_indicators(df):
    close = df['price']
    volume = df['volume']

    # RSI
    rsi = ta.momentum.RSIIndicator(close=close, window=14).rsi()
    # ATR needs high, low, close; if missing high/low, use +/- 1%
    if 'high' in df.columns and 'low' in df.columns:
        high = df['high'].astype(float)
        low = df['low'].astype(float)
    else:
        high = close * 1.01
        low = close * 0.99
    atr = ta.volatility.AverageTrueRange(high=high, low=low, close=close, window=14).average_true_range()
    bb_indicator = ta.volatility.BollingerBands(close=close, window=20)
    bb_width = (bb_indicator.bollinger_hband() - bb_indicator.bollinger_lband()) / bb_indicator.bollinger_mavg()
    ma_5 = close.rolling(window=5).mean()
    ma_10 = close.rolling(window=10).mean()
    ma_20 = close.rolling(window=20).mean()
    returns_1 = close.pct_change(1).fillna(0)
    returns_3 = close.pct_change(3).fillna(0)
    returns_7 = close.pct_change(7).fillna(0)

    df['rsi'] = rsi.fillna(method='bfill')
    df['atr'] = atr.fillna(method='bfill')
    df['bb_width'] = bb_width.fillna(method='bfill')
    df['ma_5'] = ma_5.fillna(method='bfill')
    df['ma_10'] = ma_10.fillna(method='bfill')
    df['ma_20'] = ma_20.fillna(method='bfill')
    df['returns_1'] = returns_1
    df['returns_3'] = returns_3
    df['returns_7'] = returns_7

    return df

def create_features(df, window=5):
    X, y = [], []
    feature_cols = ['price', 'volume', 'rsi', 'atr', 'bb_width', 'ma_5', 'ma_10', 'ma_20', 'returns_1', 'returns_3', 'returns_7']
    for i in range(window, len(df) - 1):
        features = []
        for j in range(window):
            row = df.iloc[i - window + j]
            features.extend([row[col] for col in feature_cols])
        X.append(features)
        y.append(df.iloc[i + 1]['price'])
    return np.array(X), np.array(y)

def train_and_tune(data_file='binance_btc_3yrs_chunked.json'):
    logging.info(f"Loading data from {data_file}")
    df = load_data(data_file)
    df = add_technical_indicators(df)
    X, y = create_features(df)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    param_dist = {
        'n_estimators': [100, 200, 300, 400],
        'max_depth': [10, 20, 30, 40, None],
        'min_samples_split': [2, 3, 5, 10],
        'min_samples_leaf': [1, 2, 4, 6]
    }

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    model = RandomForestRegressor(random_state=42)
    rand_search = RandomizedSearchCV(
        model,
        param_distributions=param_dist,
        n_iter=25,
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

    joblib.dump(best_model, 'trained_model.joblib')
    joblib.dump(scaler, 'scaler.joblib')

    print(f"Best hyperparameters: {rand_search.best_params_}")
    print(f"Mean Squared Error on test set: {mse:.4f}")

if __name__ == "__main__":
    train_and_tune()
