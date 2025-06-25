import React, { useEffect, useState } from "react";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [activeStrategies, setActiveStrategies] = useState([]);

  useEffect(() => {
    fetch("/stats.json")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setActiveStrategies(json.activeStrategies);
      })
      .catch((err) => console.error("Failed to load stats:", err));
  }, []);

  const toggleStrategy = (strategy) => {
    setActiveStrategies((prev) =>
      prev.includes(strategy)
        ? prev.filter((s) => s !== strategy)
        : [...prev, strategy]
    );
  };

  if (!data) return <p className="p-6">Loading strategy data...</p>;

  const equityData = [
    { time: "Day 1", value: 500 },
    { time: "Day 2", value: 520 },
    { time: "Day 3", value: 510 },
    { time: "Day 4", value: 530 },
    { time: "Day 5", value: 545 },
    { time: "Day 6", value: 560 },
    { time: "Day 7", value: 575 },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
      <Card>
        <CardContent>
          <h2 className="text-xl font-semibold mb-4">Active Strategies</h2>
          {activeStrategies.map((strategy, idx) => (
            <Badge key={idx} className="mr-2">{strategy}</Badge>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-xl font-semibold mb-4">Recommended Strategy</h2>
          <Badge className="text-lg p-2">{data.recommendedStrategy}</Badge>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-lg font-medium mb-2">PnL</h2>
          <p className="text-2xl font-bold">{data.pnl}</p>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-lg font-medium mb-2">Win Rate</h2>
          <p className="text-2xl font-bold">{data.winRate}</p>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-lg font-medium mb-2">Sharpe Ratio</h2>
          <p className="text-2xl font-bold">{data.sharpeRatio}</p>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-lg font-medium mb-2">Profit Factor</h2>
          <p className="text-2xl font-bold">{data.profitFactor}</p>
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-2">
        <CardContent>
          <h2 className="text-xl font-semibold mb-4">Equity Curve</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={equityData}>
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="col-span-1 md:col-span-2">
        <CardContent>
          <h2 className="text-xl font-semibold mb-4">Toggle Strategies</h2>
          {["MACD-Trend", "RSI-Reversal", "ADX-Filter"].map((strategy) => (
            <Button
              key={strategy}
              className="mr-3 mb-3"
              variant={activeStrategies.includes(strategy) ? "default" : "outline"}
              onClick={() => toggleStrategy(strategy)}
            >
              {activeStrategies.includes(strategy) ? `✅ ${strategy}` : `➕ ${strategy}`}
            </Button>
          ))}
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;
