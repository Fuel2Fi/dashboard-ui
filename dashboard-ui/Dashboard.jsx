import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
} from "chart.js";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import MetricCard from "../components/MetricCard";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

function Dashboard() {
  const [selectedMenu, setSelectedMenu] = useState("Dashboard");
  const [stats, setStats] = useState({
    pnl: "+0%",
    winRate: "0%",
    sharpeRatio: "0",
    profitFactor: "0"
  });
  const [trades, setTrades] = useState([]);

  // Fetch stats and trades on mount and every 10 seconds
  useEffect(() => {
    fetch("/api/stats")
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(console.error);

    fetch("/api/trades")
      .then(res => res.json())
      .then(data => setTrades(data))
      .catch(console.error);

    const interval = setInterval(() => {
      fetch("/api/stats")
        .then(res => res.json())
        .then(data => setStats(data))
        .catch(console.error);
      fetch("/api/trades")
        .then(res => res.json())
        .then(data => setTrades(data))
        .catch(console.error);
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  // Prepare chart data from trades
  const chartData = {
    labels: trades.map(trade => trade.timestamp),
    datasets: [
      {
        label: "PnL Over Time",
        data: trades.map(trade => parseFloat(trade.pnl) || 0),
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.3
      }
    ]
  };

  return (
    <div className="flex flex-col h-screen">
      <Header userName="Boss" />
      <div className="flex flex-1">
        <Sidebar selected={selectedMenu} onSelect={setSelectedMenu} />
        <main className="flex-1 p-6 bg-gray-50 overflow-auto">
          {selectedMenu === "Dashboard" && (
            <section>
              <h2 className="text-2xl font-semibold mb-4">Key Metrics</h2>
              <div className="flex flex-wrap mb-6">
                <MetricCard label="PnL" value={stats.pnl} />
                <MetricCard label="Win Rate" value={stats.winRate} />
                <MetricCard label="Sharpe Ratio" value={stats.sharpeRatio} />
                <MetricCard label="Profit Factor" value={stats.profitFactor} />
              </div>

              <div className="mb-10">
                <Line data={chartData} />
              </div>

              <h2 className="text-xl font-semibold mb-4">Recent Trades</h2>
              <table className="min-w-full border border-gray-300 bg-white rounded-md">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-2 border-b">Timestamp</th>
                    <th className="px-4 py-2 border-b">Symbol</th>
                    <th className="px-4 py-2 border-b">Side</th>
                    <th className="px-4 py-2 border-b">Price</th>
                    <th className="px-4 py-2 border-b">Quantity</th>
                    <th className="px-4 py-2 border-b">PnL</th>
                  </tr>
                </thead>
                <tbody>
                  {trades.map((trade, idx) => (
                    <tr key={idx} className="text-center">
                      <td className="border-b px-4 py-2">{trade.timestamp}</td>
                      <td className="border-b px-4 py-2">{trade.symbol}</td>
                      <td className="border-b px-4 py-2">{trade.side}</td>
                      <td className="border-b px-4 py-2">{trade.price}</td>
                      <td className="border-b px-4 py-2">{trade.quantity}</td>
                      <td className="border-b px-4 py-2">{trade.pnl || "N/A"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          )}
          {selectedMenu === "Settings" && (
            <section>
              <h2 className="text-2xl font-semibold mb-4">Settings (Coming Soon)</h2>
            </section>
          )}
          {selectedMenu === "Logs" && (
            <section>
              <h2 className="text-2xl font-semibold mb-4">Logs (Coming Soon)</h2>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
