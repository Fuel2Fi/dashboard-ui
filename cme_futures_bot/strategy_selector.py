import pandas as pd
from strategy_trend_following import analyze as trend_following_analyze
from strategy_mean_reversion import analyze as mean_reversion_analyze
from strategy_breakout import analyze as breakout_analyze
from strategy_gaussian_macd import analyze as gaussian_macd_analyze
from strategy_rsi_divergence import analyze as rsi_divergence_analyze

def run_selected_strategy(df: pd.DataFrame, strategy: str) -> pd.DataFrame:
    """
    Dispatches the dataframe to the selected strategy.
    """
    if strategy == "trend_following":
        return trend_following_analyze(df)
    elif strategy == "mean_reversion":
        return mean_reversion_analyze(df)
    elif strategy == "breakout":
        return breakout_analyze(df)
    elif strategy == "gaussian_macd":
        return gaussian_macd_analyze(df)
    elif strategy == "rsi_divergence":
        return rsi_divergence_analyze(df)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
