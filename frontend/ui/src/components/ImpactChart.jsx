import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function ImpactChart({ data }) {
  const chartData = [
    { name: "Before", value: data.before.length },
    { name: "After", value: data.after.length }
  ];

  return (
    <div className="chart">
      <BarChart width={300} height={200} data={chartData}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" />
      </BarChart>
    </div>
  );
}