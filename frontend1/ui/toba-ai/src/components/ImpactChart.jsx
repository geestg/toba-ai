import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

export default function ImpactChart({ data }) {
  const chartData = data || [
    { name: "Sebelum", crowd: 80 },
    { name: "Sesudah", crowd: 40 },
  ];

  const colors = ["#f29b39", "#2f9a93"];

  return (
    <div className="impact-chart animate-fade-in-scale">
      <div className="chart-header">
        <span className="chart-icon">📊</span>
        <h3>Dampak Wisata</h3>
      </div>

      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={chartData} barSize={48}>
          <XAxis
            dataKey="name"
            tick={{ fontSize: 13, fill: "#5f6f80" }}
            axisLine={{ stroke: "#e2e8f0" }}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 12, fill: "#8a9aab" }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            contentStyle={{
              background: "#fff",
              border: "1px solid #e2e8f0",
              borderRadius: "12px",
              fontSize: "13px",
              boxShadow: "0 8px 24px rgba(12,35,56,0.1)",
            }}
          />
          <Bar dataKey="crowd" radius={[8, 8, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

