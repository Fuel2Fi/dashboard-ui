#!/usr/bin/env python3
import pandas as pd
from datetime import datetime

# Load signals
signals_df = pd.read_csv('./data/lstm_trade_signals.csv')

# Initialize trade log
trade_log = []

# Track current positions
positions = {col: 'NONE' for col in signals_df.columns if col != 'timestamp'}

# Fixed parameters
position_size = 1000  # USD
price_move_per_step = 0.01  # 1% assumed price movement per time step

# Process each timestamp row
for idx, row in signals_df.iterrows():
    timestamp = row['timestamp']
    for symbol in positions.keys():
        signal = row[symbol]
        current_position = positions[symbol]
        pnl = 0.0
        action = 'HOLD'

        if signal == 'BUY':
            if current_position == 'NONE':
                positions[symbol] = 'LONG'
                action = 'OPEN_LONG'
            elif current_position == 'SHORT':
                positions[symbol] = 'LONG'
                pnl = position_size * 2 * price_move_per_step
                action = 'CLOSE_SHORT_OPEN_LONG'

        elif signal == 'SELL':
            if current_position == 'NONE':
                positions[symbol] = 'SHORT'
                action = 'OPEN_SHORT'
            elif current_position == 'LONG':
                positions[symbol] = 'SHORT'
                pnl = position_size * 2 * price_move_per_step
                action = 'CLOSE_LONG_OPEN_SHORT'

        elif signal == 'HOLD':
            action = 'HOLD'

        # Record trade
        trade_log.append({
            'timestamp': timestamp,
            'symbol': symbol,
            'signal': signal,
            'action': action,
            'position_after': positions[symbol],
            'pnl_this_step': pnl
        })

# Save log
log_df = pd.DataFrame(trade_log)
log_df.to_csv('./data/lstm_trade_simulation_log.csv', index=False)

print('✅ Simulation complete. Log saved to ./data/lstm_trade_simulation_log.csv.')
