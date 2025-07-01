import csv
import os
from datetime import datetime, timezone

LOG_FILE = "trade_log.csv"

# Ensure log file exists with headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "symbol",
            "side",
            "quantity",
            "price",
            "strategy",
            "reason"
        ])

def log_trade(symbol, side, qty, price, strategy, reason):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            symbol,
            side,
            qty,
            price,
            strategy,
            reason
        ])
    print(f"✅ Trade logged: {symbol} {side} {qty} at {price} ({reason})")

if __name__ == "__main__":
    # Example test log
    log_trade("BTCUSDT", "BUY", 0.01, 30000, "momentum", "ENTRY_TEST")
