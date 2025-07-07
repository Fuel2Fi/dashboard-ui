import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

def main():
    # Load trade log
    df = pd.read_csv("trade_performance_log.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    # Compute performance metrics
    total_trades = df["Status"].str.contains("Exit").sum()
    wins = df["Status"].str.contains("Exit triggered").sum() - df[df["Status"].str.contains("PnL: -")]["Status"].count()
    losses = total_trades - wins
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    cumulative_profit = df["CumulativeProfit"].iloc[-1] if not df.empty else 0
    avg_return = (cumulative_profit / total_trades) if total_trades > 0 else 0

    # Create equity curve plot
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["CumulativeProfit"], color="blue", label="Equity Curve")

    for idx, row in df.iterrows():
        date = row["Date"]
        profit = row["CumulativeProfit"]
        status = row["Status"]

        if "Entry" in status:
            plt.scatter(date, profit, color="green", marker="^", s=70)
        elif "Exit" in status:
            plt.scatter(date, profit, color="red", marker="v", s=70)
            try:
                pnl_str = status.split("PnL:")[1].replace(")", "").strip()
                plt.text(date, profit - 30, f"{pnl_str}", color="black", fontsize=8, ha="center")
            except IndexError:
                pass

    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Profit")
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)

    # Save plot image
    plot_filename = "equity_curve_temp.png"
    plt.savefig(plot_filename)
    plt.close()

    # Generate PDF report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"performance_report_{timestamp}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Trading Strategy Performance Report")

    # Summary
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 110, f"Total Trades: {total_trades}")
    c.drawString(50, height - 130, f"Wins: {wins}")
    c.drawString(50, height - 150, f"Losses: {losses}")
    c.drawString(50, height - 170, f"Win Rate: {win_rate:.2f}%")
    c.drawString(50, height - 190, f"Average Return per Trade: {avg_return:.2f}")
    c.drawString(50, height - 210, f"Cumulative Profit: {cumulative_profit:.2f}")

    # Insert equity curve
    c.drawImage(plot_filename, 50, 100, width=500, height=300)

    c.save()
    print(f"✅ Performance report generated: {pdf_filename}")

if __name__ == "__main__":
    main()
