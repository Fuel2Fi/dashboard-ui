import pandas as pd
import numpy as np
import ta

# Load historical data
df = pd.read_csv('historical_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Gaussian Channel Calculation (custom example)
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

    # Example: Buy if close above Gaussian Upper and RSI < 70 and MACD > MACD_Signal
    if (
        row['Close'] > row['Gaussian_Upper']
        and row['RSI'] < 70
        and row['MACD'] > row['MACD_Signal']
    ):
        signal = "BUY"

    # Example: Sell if close below Gaussian Lower and RSI > 30 and MACD < MACD_Signal
    elif (
        row['Close'] < row['Gaussian_Lower']
        and row['RSI'] > 30
        and row['MACD'] < row['MACD_Signal']
    ):
        signal = "SELL"

    signals.append(signal)

df['Signal'] = signals

# Display output
print(df[['Open','High','Low','Close','Gaussian_Upper','Gaussian_Lower','ATR','ADX','MACD','MACD_Signal','RSI','Signal']])

# Save signals to CSV
df.to_csv('strategy_signals_output.csv')

print("\n✅ Strategy signals saved to 'strategy_signals_output.csv'")
