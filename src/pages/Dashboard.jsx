import React, { useEffect, useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const metrics = ["PnL", "Win Rate", "Sharpe Ratio", "Profit Factor"];

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Replace this with a real API fetch later
    setStats({
      activeStrategies: ["MACD-Trend", "RSI-Reversal"],
      recommendedStrategy: "MACD-Trend",
      pnl: "+12.5%",
      winRate: "67%",
      sharpeRatio: "1.4",
      profitFactor: "2.3",
    });
  }, []);

  if (!stats) return <div className="p-6 text-lg">Loading...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
      <Card>
        <CardContent>
          <h2 className="text-xl font-semibold mb-4">Active Strategies</h2>
          {stats.activeStrategies.map((strat, i) => (
            <Badge key={i} className="mr-2 mb-2">{strat}</Badge>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-xl font-semibold mb-4">Recommended Strategy</h2>
          <Badge className="text-lg p-2">{stats.recommendedStrategy}</Badge>
        </CardContent>
      </Card>

      {metrics.map((label) => (
        <Card key={label}>
          <CardContent>
            <h2 className="text-lg font-medium">{label}</h2>
            <p className="text-2xl mt-2 font-bold">
              {stats[label.toLowerCase().replace(" ", "")]}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
