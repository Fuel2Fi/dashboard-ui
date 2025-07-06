import pandas as pd

def get_consensus_signal(strategy_results: dict, required_agreement: int) -> pd.DataFrame:
    """
    Aggregates signals from multiple strategies and returns consensus.

    Args:
        strategy_results (dict):
            Keys = strategy names,
            Values = DataFrames with 'Signal' column indexed by date.
        required_agreement (int): Number of strategies that must agree to act.

    Returns:
        DataFrame with consensus signal.
    """
    # Start with index of the first strategy
    base_index = next(iter(strategy_results.values())).index

    consensus = []
    for idx in base_index:
        signals_today = []
        for df in strategy_results.values():
            if idx in df.index:
                signals_today.append(df.loc[idx, "Signal"])

        # Count occurrences
        buy_count = signals_today.count("BUY")
        sell_count = signals_today.count("SELL")

        if buy_count >= required_agreement:
            consensus_signal = "BUY"
        elif sell_count >= required_agreement:
            consensus_signal = "SELL"
        else:
            consensus_signal = "HOLD"

        consensus.append({
            "Date": idx,
            "ConsensusSignal": consensus_signal
        })

    consensus_df = pd.DataFrame(consensus)
    consensus_df.set_index("Date", inplace=True)
    return consensus_df
