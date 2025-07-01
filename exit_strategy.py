import json
import os
from datetime import datetime, timezone
from config import API_KEY, API_SECRET
from binance.spot import Spot
from trade_logger import log_trade

client = Spot(api_key=API_KEY, api_secret=API_SECRET)

POSITIONS_FILE = "positions.json"

STOP_LOSS_PCT = 0.02
TAKE_PROFIT_PCT = 0.04
TRAILING_SL_PCT = 0.015
TRAILING_TP_PCT = 0.02

def load_positions():
    if not os.path.exists(POSITIONS_FILE):
        return {}
    with open(POSITIONS_FILE, "r") as f:
        return json.load(f)

def save_positions(positions):
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=2)

def check_and_exit():
    positions = load_positions()
    symbols_to_remove = []
    for symbol, pos in positions.items():
        entry = pos["entry_price"]
        side = pos["side"]
        qty = pos["quantity"]
        strategy = pos.get("strategy", "unknown")

        ticker = client.ticker_price(symbol=symbol)
        current_price = float(ticker["price"])

        exit_reason = None

        if side == "BUY":
            stop_loss = entry * (1 - STOP_LOSS_PCT)
            take_profit = entry * (1 + TAKE_PROFIT_PCT)

            if current_price <= stop_loss:
                exit_reason = "STOP_LOSS"
            elif current_price >= take_profit:
                exit_reason = "TAKE_PROFIT"
            else:
                if current_price > pos.get("highest_price", entry):
                    pos["highest_price"] = current_price
                trailing_stop = pos["highest_price"] * (1 - TRAILING_SL_PCT)
                if current_price <= trailing_stop:
                    exit_reason = "TRAILING_STOP"

        elif side == "SELL":
            stop_loss = entry * (1 + STOP_LOSS_PCT)
            take_profit = entry * (1 - TAKE_PROFIT_PCT)

            if current_price >= stop_loss:
                exit_reason = "STOP_LOSS"
            elif current_price <= take_profit:
                exit_reason = "TAKE_PROFIT"
            else:
                if current_price < pos.get("lowest_price", entry):
                    pos["lowest_price"] = current_price
                trailing_stop = pos["lowest_price"] * (1 + TRAILING_TP_PCT)
                if current_price >= trailing_stop:
                    exit_reason = "TRAILING_STOP"

        if exit_reason:
            try:
                side_exit = "SELL" if side == "BUY" else "BUY"
                order = client.new_order(
                    symbol=symbol,
                    side=side_exit,
                    type="MARKET",
                    quantity=qty
                )
                print(f"✅ {symbol}: Exit order placed ({exit_reason}).")
                log_trade(symbol, side_exit, qty, current_price, strategy, exit_reason)
                symbols_to_remove.append(symbol)
            except Exception as e:
                print(f"❌ {symbol}: Error placing exit order: {e}")

    for s in symbols_to_remove:
        del positions[s]

    save_positions(positions)

if __name__ == "__main__":
    check_and_exit()
