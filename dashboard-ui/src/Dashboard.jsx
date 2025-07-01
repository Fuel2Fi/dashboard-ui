import React, { useEffect, useState } from "react";

function Dashboard() {
  const [trades, setTrades] = useState([]);
  const [balance, setBalance] = useState(null);
  const [strategy, setStrategy] = useState(null);

  useEffect(() => {
    fetch("/api/trades")
      .then(res => res.json())
      .then(data => setTrades(data.trades || []));

    fetch("/api/balance")
      .then(res => res.json())
      .then(data => setBalance(data.usdt));

    fetch("/api/strategy")
      .then(res => res.json())
      .then(data => setStrategy(data.consensus?.method || "Unknown"));
  }, []);

  return (
    <div className="dark bg-gray-900 text-white min-h-screen p-6">
      <h1 className="text-3xl font-bold mb-4">Fuel2Fi Trading Dashboard</h1>
      <section className="mb-6">
        <h2 className="text-xl font-semibold">Account Balance</h2>
        <p className="text-green-400">{balance !== null ? `$${balance} USDT` : "Loading..."}</p>
      </section>
      <section className="mb-6">
        <h2 className="text-xl font-semibold">Active Strategy</h2>
        <p>{strategy}</p>
      </section>
      <section>
        <h2 className="text-xl font-semibold mb-2">Recent Trades</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full table-auto border-collapse">
            <thead>
              <tr className="bg-gray-700">
                <th className="px-4 py-2 text-left">Time</th>
                <th className="px-4 py-2 text-left">Symbol</th>
                <th className="px-4 py-2 text-left">Signal</th>
                <th className="px-4 py-2 text-left">Result</th>
              </tr>
            </thead>
            <tbody>
              {trades.length === 0 ? (
                <tr>
                  <td colSpan="4" className="text-center py-4">No trades yet.</td>
                </tr>
              ) : (
                trades.map((trade, index) => (
                  <tr key={index} className="border-t border-gray-600">
                    <td className="px-4 py-2">{trade.timestamp}</td>
                    <td className="px-4 py-2">{trade.symbol}</td>
                    <td className="px-4 py-2">
                      <span
                        className={
                          trade.signal === "BUY"
                            ? "text-green-400"
                            : trade.signal === "SELL"
                            ? "text-red-400"
                            : "text-yellow-400"
                        }
                      >
                        {trade.signal}
                      </span>
                    </td>
                    <td className="px-4 py-2">{trade.result}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
