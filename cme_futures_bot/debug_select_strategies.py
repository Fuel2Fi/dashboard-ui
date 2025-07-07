from strategy_switcher import select_strategies

selected_strategies = select_strategies()

print("✅ Raw output of select_strategies():")
for idx, item in enumerate(selected_strategies, 1):
    print(f"{idx}: {item}")
