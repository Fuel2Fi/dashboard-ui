import pandas as pd

def select_top_strategies(performance_csv_paths: dict, top_n: int) -> list:
    """
    Reads multiple strategy performance CSVs, ranks them by Sharpe Ratio,
    and returns the names of the top N strategies to activate.

    Args:
        performance_csv_paths (dict):
            Keys = strategy names,
            Values = CSV paths with 'Sharpe' column.
        top_n (int): Number of strategies to activate.

    Returns:
        List of strategy names.
    """
    scores = []
    for name, csv_path in performance_csv_paths.items():
        try:
            df = pd.read_csv(csv_path)
            # Use the last Sharpe ratio
            last_row = df.iloc[-1]
            sharpe = float(last_row["Sharpe"])
            scores.append((name, sharpe))
        except Exception as e:
            print(f"⚠️ Error reading {csv_path}: {e}")
            # Assign very low Sharpe if error
            scores.append((name, -999))

    # Sort strategies descending by Sharpe
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)
    top_strategies = [name for name, _ in ranked[:top_n]]

    print("\n✅ Strategy Switcher Selection:")
    for i, (name, sharpe) in enumerate(ranked, 1):
        print(f"{i}. {name} - Sharpe: {sharpe:.2f}")
    print(f"\n🎯 Active strategies: {top_strategies}\n")

    return top_strategies
