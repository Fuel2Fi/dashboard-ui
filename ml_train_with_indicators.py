import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import ta  # Technical Analysis library

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def add_indicators(df):
    # Price series
    close = df['price']

    # RSI
    df['rsi'] = ta.momentum.RSIIndicator(close, window=14).rsi()

    # MACD
    macd = ta.trend.MACD(close)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()

    # ATR
    # For ATR we need high, low, close - simulate high/low as close +/- small random noise
    np.random.seed(42)
    df['high'] = close * (1 + np.random.uniform(0, 0.01, size=len(df)))
    df['low'] = close * (1 - np.random.uniform(0, 0.01, size=len(df)))
    atr = ta.volatility.AverageTrueRange(df['high'], df['low'], close, window=14)
    df['atr'] = atr.average_true_range()

    # Fill NaNs after indicator calculation
    df.fillna(method='bfill', inplace=True)

    return df

def create_features(df, window=5):
    X, y = [], []
    for i in range(window, len(df)-1):
        features = []
        for j in range(i-window, i):
            features.extend([
                df.iloc[j]['price'],
                df.iloc[j]['rsi'],
                df.iloc[j]['macd_diff'],
                df.iloc[j]['atr'],
            ])
        X.append(features)
        y.append(df.iloc[i]['price'])
    return np.array(X), np.array(y)

def main():
    df = load_data('mock_price_data.json')
    df = add_indicators(df)
    X, y = create_features(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
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
