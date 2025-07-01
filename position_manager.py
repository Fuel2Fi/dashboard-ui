import json
import os
from datetime import datetime, timezone

POSITIONS_FILE = "positions.json"

def load_positions():
    if not os.path.exists(POSITIONS_FILE):
        return []
    with open(POSITIONS_FILE, "r") as f:
        return json.load(f)

def save_positions(positions):
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=2)

def add_position(symbol, entry_price, quantity, strategy, stop_loss_pct=0.03, take_profit_pct=0.05, trailing_pct=0.02):
    positions = load_positions()
    positions.append({
        "symbol": symbol,
        "entry_price": entry_price,
        "quantity": quantity,
        "strategy": strategy,
        "stop_loss_pct": stop_loss_pct,
        "take_profit_pct": take_profit_pct,
        "trailing_pct": trailing_pct,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "highest_price": entry_price  # for trailing stops
    })
    save_positions(positions)
    print(f"✅ Added position: {symbol} {quantity} at {entry_price}")

def update_highest_price(symbol, current_price):
    positions = load_positions()
    updated = False
    for pos in positions:
        if pos["symbol"] == symbol:
            if current_price > pos["highest_price"]:
                pos["highest_price"] = current_price
                updated = True
    if updated:
        save_positions(positions)

def remove_position(symbol):
    positions = load_positions()
    positions = [p for p in positions if p["symbol"] != symbol]
    save_positions(positions)
    print(f"✅ Removed position: {symbol}")
