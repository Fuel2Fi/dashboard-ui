export default function MetricCard({ label, value }) {
  return (
    <div className="bg-white p-4 m-2 rounded shadow w-48">
      <div className="text-gray-500">{label}</div>
      <div className="text-2xl font-bold">{value}</div>
    </div>
  );
}
