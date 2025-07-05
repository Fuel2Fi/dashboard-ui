import pandas as pd
import ta

def analyze(df: pd.DataFrame) -> pd.DataFrame:
    # Gaussian Channel
    gaussian_window = 10
    df['Gaussian_Upper'] = df['Close'].rolling(window=gaussian_window).mean() + 2 * df['Close'].rolling(window=gaussian_window).std()
    df['Gaussian_Lower'] = df['Close'].rolling(window=gaussian_window).mean() - 2 * df['Close'].rolling(window=gaussian_window).std()

    # ATR
    atr = ta.volatility.AverageTrueRange(
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        window=14
    )
    df['ATR'] = atr.average_true_range()

    # ADX
    adx = ta.trend.ADXIndicator(
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        window=14
    )
    df['ADX'] = adx.adx()

    # MACD
    macd = ta.trend.MACD(
        close=df['Close'],
        window_slow=26,
        window_fast=12,
        window_sign=9
    )
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()

    # RSI
    rsi = ta.momentum.RSIIndicator(
        close=df['Close'],
        window=14
    )
    df['RSI'] = rsi.rsi()

    # Signal Logic
    signals = []
    for idx, row in df.iterrows():
        signal = "HOLD"
        if (
            row['Close'] > row['Gaussian_Upper']
            and row['RSI'] < 70
            and row['MACD'] > row['MACD_Signal']
        ):
            signal = "BUY"
        elif (
            row['Close'] < row['Gaussian_Lower']
            and row['RSI'] > 30
            and row['MACD'] < row['MACD_Signal']
        ):
            signal = "SELL"
        signals.append(signal)

    df['Signal'] = signals
    return df
