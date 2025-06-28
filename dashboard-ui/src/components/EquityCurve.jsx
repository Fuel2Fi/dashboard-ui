import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

function EquityCurve({ data }) {
  if (!data || data.length === 0) return <p>No equity curve data available.</p>;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="timestamp" tickFormatter={(tick) => new Date(tick).toLocaleTimeString()} />
        <YAxis domain={['auto', 'auto']} />
        <Tooltip labelFormatter={(label) => new Date(label).toLocaleString()} />
        <Legend />
        <Line type="monotone" dataKey="value" stroke="#4ade80" strokeWidth={3} dot={false} name="Equity Curve" />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default EquityCurve;
