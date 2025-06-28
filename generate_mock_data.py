import json
import random
from datetime import datetime, timedelta

def generate_mock_price_data(start_date, days, start_price=100.0):
    data = []
    current_price = start_price
    current_date = start_date

    for _ in range(days):
        # Simulate daily % change -1% to +1%
        pct_change = random.uniform(-0.01, 0.01)
        current_price *= (1 + pct_change)
        current_price = round(current_price, 2)
        data.append({
            "timestamp": current_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "price": current_price
        })
        current_date += timedelta(days=1)
    return data

if __name__ == "__main__":
    start_date = datetime(2025, 1, 1)
    days = 180  # 6 months of daily data
    mock_data = generate_mock_price_data(start_date, days)
    with open("mock_price_data.json", "w") as f:
        json.dump(mock_data, f, indent=2)
    print(f"Mock price data for {days} days generated in mock_price_data.json")
