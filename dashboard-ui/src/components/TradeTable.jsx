export default function TradeTable({ trades }) {
  return (
    <table className="min-w-full bg-white rounded shadow">
      <thead>
        <tr>
          <th className="border px-4 py-2">Timestamp</th>
          <th className="border px-4 py-2">Symbol</th>
          <th className="border px-4 py-2">Side</th>
          <th className="border px-4 py-2">Price</th>
          <th className="border px-4 py-2">Quantity</th>
          <th className="border px-4 py-2">PnL</th>
        </tr>
      </thead>
      <tbody>
        {trades.map((trade) => (
          <tr key={trade.id}>
            <td className="border px-4 py-2">{trade.timestamp}</td>
            <td className="border px-4 py-2">{trade.symbol}</td>
            <td className="border px-4 py-2">{trade.side}</td>
            <td className="border px-4 py-2">{trade.price}</td>
            <td className="border px-4 py-2">{trade.quantity}</td>
            <td className="border px-4 py-2">{trade.pnl ?? "N/A"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
