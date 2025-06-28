import React from "react";
import useWebSocketStats from "./components/useWebSocketStats";
import EquityCurve from "./components/EquityCurve";

function Dashboard() {
  const stats = useWebSocketStats();

  if (!stats) return <p>Loading stats...</p>;

  return (
    <div>
      <h1>Trading Bot Dashboard</h1>
      <div className="metrics">
        <div><strong>PnL</strong><br />{stats.pnl}</div>
        <div><strong>Win Rate</strong><br />{stats.winRate}</div>
        <div><strong>Sharpe Ratio</strong><br />{stats.sharpeRatio}</div>
        <div><strong>Profit Factor</strong><br />{stats.profitFactor}</div>
      </div>
      <h2>Equity Curve</h2>
      <EquityCurve data={stats.equityCurve} />
    </div>
  );
}

export default Dashboard;
