import json
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import AverageTrueRange
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold
from sklearn.metrics import mean_squared_error

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['open'] = df['open'].astype(float)
    return df

def add_technical_indicators(df):
    df['rsi'] = RSIIndicator(df['close']).rsi()
    macd = MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_hist'] = macd.macd_diff()
    df['atr'] = AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
    df.fillna(method='bfill', inplace=True)  # backfill to handle NaNs
    return df

def create_features(df, window=5):
    X, y = [], []
    for i in range(window, len(df)-1):
        features = []
        # Add price window
        features.extend(df['close'].iloc[i-window:i].values)
        # Add RSI, MACD histogram, ATR at current index
        features.append(df['rsi'].iloc[i])
        features.append(df['macd_hist'].iloc[i])
        features.append(df['atr'].iloc[i])
        X.append(features)
        y.append(df['close'].iloc[i+1])
    return np.array(X), np.array(y)

def main():
    df = load_data('binance_historical_data.json')
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
    rand_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=10, cv=cv,
                                     scoring='neg_mean_squared_error', random_state=42, n_jobs=-1)
    rand_search.fit(X_train, y_train)

    best_model = rand_search.best_estimator_
    preds = best_model.predict(X_test)
    mse = mean_squared_error(y_test, preds)

    print(f"Best hyperparameters: {rand_search.best_params_}")
    print(f"Mean Squared Error on test set: {mse:.4f}")

    example_input = X_test[0].reshape(1, -1)
    prediction = best_model.predict(example_input)[0]
    print(f"Predicted next price: {prediction:.2f}")
    print(f"Actual next price: {y_test[0]:.2f}")

if __name__ == "__main__":
    main()
