import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function ImpactChart() {
  const data = [
    { name: "Sebelum", crowd: 80 },
    { name: "Sesudah", crowd: 40 }
  ];

  return (
    <div className="chart">
      <h3>Impact Wisata</h3>

      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="crowd" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}