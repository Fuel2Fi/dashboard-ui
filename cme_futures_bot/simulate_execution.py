import pandas as pd
from exit_strategy import ExitStrategy

# Load your price data
df = pd.read_csv("your_price_data.csv", parse_dates=["Date"], index_col="Date")

exit_engine = ExitStrategy(
    trailing_stop_pct=2.0,
    trailing_take_profit_pct=3.5,
    time_exit_candles=20
)

# Example: simulate a single long position starting on the first row
entry_date = df.index[0]
entry_price = df.iloc[0]["Close"]
symbol = "SIMULATED"

# Initialize position
exit_engine.update_position(symbol, entry_date, entry_price, "BUY", entry_price)

log_rows = []

# Iterate through the rest of the data
for date, row in df.iloc[1:].iterrows():
    current_price = row["Close"]
    exit_result = exit_engine.update_position(
        symbol,
        date,
        current_price,
        "BUY",
        entry_price
    )

    if exit_result:
        log_rows.append(exit_result)
        break  # Stop simulation after exit for this example

# Save the exit log
if log_rows:
    log_df = pd.DataFrame(log_rows)
    log_df.to_csv("exit_simulation_log.csv", index=False)
    print("✅ Exit simulation complete. Log saved to 'exit_simulation_log.csv'.")
else:
    print("✅ No exit triggered during simulation.")
