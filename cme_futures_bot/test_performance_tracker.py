from performance_tracker import PerformanceTracker

def main():
    tracker = PerformanceTracker()

    # Log some dummy trades
    tracker.log_trade(
        date="2025-07-05",
        strategy="breakout",
        signal="BUY",
        entry_price=100,
        exit_price=110
    )
    tracker.log_trade(
        date="2025-07-06",
        strategy="breakout",
        signal="SELL",
        entry_price=110,
        exit_price=100
    )
    tracker.log_trade(
        date="2025-07-07",
        strategy="trend_following",
        signal="BUY",
        entry_price=105,
        exit_price=108
    )

    # Compute stats
    stats = tracker.compute_stats()
    print("\n✅ Strategy Performance Stats:")
    for k, v in stats.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
