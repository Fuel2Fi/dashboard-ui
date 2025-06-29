#!/usr/bin/env python3
import json
import os
from datetime import datetime

POSITIONS_FILE = os.path.expanduser("~/Desktop/trading_bot/data/positions.json")

def load_positions():
    """Load current positions from the JSON file."""
    if not os.path.exists(POSITIONS_FILE):
        return {}
    with open(POSITIONS_FILE, "r") as f:
        return json.load(f)

def save_positions(positions):
    """Save positions to the JSON file."""
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=4)

def update_position(symbol, side, qty, price):
    """
    Update positions after a trade.
    - symbol: e.g., "ETH/USDT"
    - side: "buy" or "sell"
    - qty: quantity traded
    - price: executed price
    """
    positions = load_positions()
    timestamp = datetime.utcnow().isoformat()

    if symbol not in positions:
        positions[symbol] = {
            "side": side,
            "qty": qty,
            "average_price": price,
            "last_updated": timestamp
        }
    else:
        pos = positions[symbol]
        if side == pos["side"]:
            # Adding to existing position
            total_qty = pos["qty"] + qty
            avg_price = (pos["average_price"] * pos["qty"] + price * qty) / total_qty
            positions[symbol] = {
                "side": side,
                "qty": total_qty,
                "average_price": avg_price,
                "last_updated": timestamp
            }
        else:
            # Reducing or closing position
            net_qty = pos["qty"] - qty
            if net_qty > 0:
                positions[symbol]["qty"] = net_qty
                positions[symbol]["last_updated"] = timestamp
            else:
                # Position closed
                del positions[symbol]

    save_positions(positions)
    print(f"✅ Position updated: {symbol} | {side.upper()} | Qty: {qty}")

if __name__ == "__main__":
    # Quick test example
    update_position("ETH/USDT", "buy", 0.01, 3500)
    print(json.dumps(load_positions(), indent=4))
