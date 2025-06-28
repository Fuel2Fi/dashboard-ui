import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

function Dashboard() {
  const [stats, setStats] = useState({
    pnl: "--",
    winRate: "--",
    sharpeRatio: "--",
    profitFactor: "--",
    equityCurve: [],
  });

  useEffect(() => {
    async function fetchStats() {
      try {
        const response = await fetch("/api/stats");
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch stats:", error);
      }
    }
    fetchStats();

    // Optional: poll every 10 seconds
    const interval = setInterval(fetchStats, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Trading Bot Dashboard</h1>

      <div className="grid grid-cols-2 gap-6 mb-10">
        <div className="p-4 border rounded shadow">
          <h2 className="text-xl font-semibold mb-2">PnL</h2>
          <p>{stats.pnl}</p>
        </div>
        <div className="p-4 border rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Win Rate</h2>
          <p>{stats.winRate}</p>
        </div>
        <div className="p-4 border rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Sharpe Ratio</h2>
          <p>{stats.sharpeRatio}</p>
        </div>
        <div className="p-4 border rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Profit Factor</h2>
          <p>{stats.profitFactor}</p>
        </div>
      </div>

      <div style={{ width: "100%", height: 300 }}>
        <h2 className="text-xl font-semibold mb-2">Equity Curve</h2>
        <ResponsiveContainer>
          <LineChart data={stats.equityCurve} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" tickFormatter={(tick) => new Date(tick).toLocaleTimeString()} />
            <YAxis />
            <Tooltip labelFormatter={(label) => new Date(label).toLocaleString()} />
            <Line type="monotone" dataKey="value" stroke="#3b82f6" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Dashboard;
