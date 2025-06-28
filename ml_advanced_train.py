import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Load price data from JSON
def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df

# Feature engineering: add returns, moving averages, volatility (std dev), ATR approximation
def create_features(df, window=5):
    df['return'] = df['price'].pct_change()
    df['ma'] = df['price'].rolling(window=window).mean()
    df['std'] = df['price'].rolling(window=window).std()
    df['volatility'] = df['return'].rolling(window=window).std()
    # Approximate ATR as rolling std dev of returns scaled by price (simplified)
    df['atr'] = df['volatility'] * df['price']
    df = df.dropna().reset_index(drop=True)

    X = []
    y = []
    for i in range(len(df) - window):
        features = []
        for j in range(window):
            features.extend([
                df.loc[i+j, 'price'],
                df.loc[i+j, 'return'],
                df.loc[i+j, 'ma'],
                df.loc[i+j, 'std'],
                df.loc[i+j, 'atr'],
            ])
        X.append(features)
        y.append(df.loc[i+window, 'price'])
    return np.array(X), np.array(y)

def main():
    df = load_data('mock_price_data.json')
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
