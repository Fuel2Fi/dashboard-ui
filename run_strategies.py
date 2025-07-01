import json
from config import API_KEY, API_SECRET
from binance.spot import Spot
from trade_logger import log_trade
from position_manager import add_position

from strategy_breakout import generate_breakout_signals
from strategy_momentum import generate_momentum_signals
from strategy_trend_following import generate_trend_signals
from strategy_volatility_expansion import generate_volatility_signals
from strategy_rsi_divergence import generate_rsi_divergence_signals
from strategy_ml_classifier import generate_ml_signals
from strategy_switcher import switch_strategies

client = Spot(api_key=API_KEY, api_secret=API_SECRET)

# Collect signals
signals = [
    generate_breakout_signals(),
    generate_momentum_signals(),
    generate_trend_signals(),
    generate_volatility_signals(),
    generate_rsi_divergence_signals(),
    generate_ml_signals()
]

print("="*60)
print("📊 Individual Strategy Signals:")
for s in signals:
    print(json.dumps(s, indent=2))

decisions = switch_strategies(signals)

print("="*60)
print("🧠 Dynamic Switching Decisions:")
print(json.dumps(decisions, indent=2))

for d in decisions["decisions"]:
    symbol = d["symbol"]
    action = d["decision"]
    if action == "hold":
        print(f"✅ {symbol}: No action (HOLD).")
        continue
    try:
        qty = 0.01
        price = float(client.ticker_price(symbol=symbol)["price"])
        if action == "buy":
            order = client.new_order(symbol=symbol, side="BUY", type="MARKET", quantity=qty)
            add_position(symbol, entry_price=price, quantity=qty, strategy="dynamic")
            log_trade(symbol, "BUY", qty, price, "dynamic", "ENTRY")
        elif action == "sell":
            order = client.new_order(symbol=symbol, side="SELL", type="MARKET", quantity=qty)
            add_position(symbol, entry_price=price, quantity=qty, strategy="dynamic")
            log_trade(symbol, "SELL", qty, price, "dynamic", "ENTRY")
        print(f"✅ {symbol}: {action.upper()} order placed.")
    except Exception as e:
        print(f"❌ {symbol}: Error placing order: {e}")
