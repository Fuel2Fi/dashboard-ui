import pandas as pd

def simulate_execution(consensus_csv_path: str):
    """
    Simulates execution based on consensus signals.
    For each signal, logs the intended action.
    """
    df = pd.read_csv(consensus_csv_path, parse_dates=["Date"])
    df.set_index("Date", inplace=True)

    positions = []
    position = None

    for date, row in df.iterrows():
        signal = row["ConsensusSignal"]

        if signal == "BUY":
            if position != "LONG":
                positions.append(f"{date.date()} - BUY signal triggered. Enter LONG position.")
                position = "LONG"
        elif signal == "SELL":
            if position != "SHORT":
                positions.append(f"{date.date()} - SELL signal triggered. Enter SHORT position.")
                position = "SHORT"
        else:
            positions.append(f"{date.date()} - HOLD. No action.")

    # Output simulation log
    for entry in positions:
        print(entry)

    # Save to file
    with open("execution_simulation_log.txt", "w") as f:
        for entry in positions:
            f.write(entry + "\n")

    print("\n✅ Simulation complete. Log saved to 'execution_simulation_log.txt'.")

if __name__ == "__main__":
    simulate_execution("consensus_signals.csv")
