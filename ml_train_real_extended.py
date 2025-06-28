import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from ta.momentum import RSIIndicator
from ta.trend import MACD

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['open_time'])
    df.set_index('timestamp', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df

def add_technical_indicators(df):
    rsi = RSIIndicator(df['close']).rsi()
    macd = MACD(df['close'])
    macd_hist = macd.macd_diff()
    df['rsi'] = rsi.fillna(method='bfill')
    df['macd_hist'] = macd_hist.fillna(method='bfill')
    return df

def create_features(df, window=5):
    X, y = [], []
    for i in range(window, len(df) - 1):
        features = []
        features.extend(df['close'].iloc[i-window:i].tolist())
        features.append(df['rsi'].iloc[i])
        features.append(df['macd_hist'].iloc[i])
        X.append(features)
        y.append(df['close'].iloc[i + 1])
    return np.array(X), np.array(y)

def main():
    df = load_data('binance_btc_3yrs_chunked.json')
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
    rand_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=10,
                                     cv=cv, scoring='neg_mean_squared_error',
                                     random_state=42, n_jobs=-1)
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

    # Save trained model for API use
    import joblib
    joblib.dump(best_model, 'trained_model.joblib')
    print("Trained model saved as trained_model.joblib")

if __name__ == "__main__":
    main()
