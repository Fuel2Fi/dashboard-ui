import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import AverageTrueRange

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['price'] = df['price'].astype(float)
    return df

def add_technical_indicators(df):
    df['return'] = df['price'].pct_change()
    df['ma'] = df['price'].rolling(window=5).mean()
    df['std'] = df['price'].rolling(window=5).std()
    df['atr'] = AverageTrueRange(high=df['price'], low=df['price'], close=df['price'], window=5).average_true_range()
    rsi = RSIIndicator(close=df['price'], window=14)
    df['rsi'] = rsi.rsi()
    macd = MACD(close=df['price'])
    df['macd_hist'] = macd.macd_diff()
    df.bfill(inplace=True)  # Future-proof fillna
    return df

def create_features(df, window=5):
    X, y = [], []
    for i in range(window, len(df) - 1):
        features = []
        for j in range(window):
            idx = i + j - window
            features.extend([
                df.loc[idx, 'price'],
                df.loc[idx, 'return'],
                df.loc[idx, 'ma'],
                df.loc[idx, 'std'],
                df.loc[idx, 'atr'],
                df.loc[idx, 'rsi'],
                df.loc[idx, 'macd_hist'],
            ])
        X.append(features)
        y.append(df.loc[i + 1, 'price'])
    return np.array(X), np.array(y)

def main():
    df = load_data('mock_price_data.json')
    df = add_technical_indicators(df)
    X, y = create_features(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Narrowed hyperparameter ranges to avoid overfitting
    param_dist = {
        'n_estimators': [50, 75, 100],
        'max_depth': [5, 10],
        'min_samples_split': [2, 4],
        'min_samples_leaf': [1, 2]
    }

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    model = RandomForestRegressor(random_state=42)
    rand_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=8, cv=cv,
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

    joblib.dump(best_model, 'trained_model.joblib')
    print("Trained model saved as trained_model.joblib")

if __name__ == "__main__":
    main()

