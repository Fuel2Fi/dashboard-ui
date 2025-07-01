#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from trade_executor import place_order, get_price

POSITIONS_FILE = "positions.json"
SIGNAL_FILE = "strategy_consensus_output.json"
TRAILING_STOP_PCT = 0.03
TRAILING_TAKE_PROFIT_PCT = 0.01

def load_positions():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_positions(positions):
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=4)

def log_trade(symbol, action, price, reason, position_type):
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f"{timestamp},{symbol},{action},{price},{reason},{position_type}\n"
    with open("trades.csv", "a") as f:
        f.write(line)

with open(SIGNAL_FILE, "r") as f:
    signals = json.load(f)

positions = load_positions()

for decision in signals["decisions"]:
    symbol = decision["symbol"]
    signal = decision["consensus_signal"]

    current_price = get_price(symbol)

    if symbol not in positions or positions[symbol]["position_type"] is None:
        if signal == "buy":
            positions[symbol] = {
                "position_type": "long",
                "entry_price": current_price,
                "high_since_entry": current_price,
                "low_since_entry": current_price,
                "trailing_stop": None,
                "take_profit": None,
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            print(f"✅ Entered LONG on {symbol} at {current_price}")
            log_trade(symbol, "ENTER", current_price, "Strategy BUY signal", "long")
            place_order(symbol, "buy")
        elif signal == "sell":
            positions[symbol] = {
                "position_type": "short",
                "entry_price": current_price,
                "high_since_entry": current_price,
                "low_since_entry": current_price,
                "trailing_stop": None,
                "take_profit": None,
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            print(f"✅ Entered SHORT on {symbol} at {current_price}")
            log_trade(symbol, "ENTER", current_price, "Strategy SELL signal", "short")
            place_order(symbol, "sell")
        else:
            print(f"✅ No holdings for {symbol}. HOLD signal.")
    else:
        pos = positions[symbol]
        if pos["position_type"] == "long":
            pos["high_since_entry"] = max(pos["high_since_entry"], current_price)
            trailing_stop = pos["high_since_entry"] * (1 - TRAILING_STOP_PCT)
            take_profit = pos["high_since_entry"] * (1 - TRAILING_TAKE_PROFIT_PCT)
            pos["trailing_stop"] = trailing_stop
            pos["take_profit"] = take_profit
            if current_price <= trailing_stop:
                print(f"✅ Trailing stop triggered on LONG {symbol} at {current_price}")
                log_trade(symbol, "EXIT", current_price, "Trailing Stop", "long")
                place_order(symbol, "sell")
                positions[symbol] = {k: None for k in pos}
            elif current_price <= take_profit:
                print(f"✅ Take profit triggered on LONG {symbol} at {current_price}")
                log_trade(symbol, "EXIT", current_price, "Take Profit", "long")
                place_order(symbol, "sell")
                positions[symbol] = {k: None for k in pos}
            else:
                print(f"✅ LONG {symbol}: price {current_price} monitored.")
        elif pos["position_type"] == "short":
            pos["low_since_entry"] = min(pos["low_since_entry"], current_price)
            trailing_stop = pos["low_since_entry"] * (1 + TRAILING_STOP_PCT)
            take_profit = pos["low_since_entry"] * (1 + TRAILING_TAKE_PROFIT_PCT)
            pos["trailing_stop"] = trailing_stop
            pos["take_profit"] = take_profit
            if current_price >= trailing_stop:
                print(f"✅ Trailing stop triggered on SHORT {symbol} at {current_price}")
                log_trade(symbol, "EXIT", current_price, "Trailing Stop", "short")
                place_order(symbol, "buy")
                positions[symbol] = {k: None for k in pos}
            elif current_price >= take_profit:
                print(f"✅ Take profit triggered on SHORT {symbol} at {current_price}")
                log_trade(symbol, "EXIT", current_price, "Take Profit", "short")
                place_order(symbol, "buy")
                positions[symbol] = {k: None for k in pos}
            else:
                print(f"✅ SHORT {symbol}: price {current_price} monitored.")

save_positions(positions)
print("✅ All positions processed and saved.")
